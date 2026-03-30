import { auth } from '@clerk/nextjs/server'

function extractMessageContent(message) {
  if (typeof message?.content === 'string') {
    return message.content
  }

  if (!Array.isArray(message?.parts)) {
    return ''
  }

  return message.parts
    .filter(part => part?.type === 'text' && typeof part.text === 'string')
    .map(part => part.text)
    .join('\n')
}

function toBackendMessages(messages = []) {
  return messages
    .map(message => ({
      role: message?.role === 'assistant' || message?.role === 'system' ? message.role : 'user',
      content: extractMessageContent(message)
    }))
    .filter(message => message.content.trim().length > 0)
}

function createLegacyProtocolTextStream(stream) {
  let buffer = ''

  return stream
    .pipeThrough(new TextDecoderStream())
    .pipeThrough(new TransformStream({
      transform(chunk, controller) {
        buffer += chunk
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (!line) continue

          if (line.startsWith('0:')) {
            try {
              controller.enqueue(JSON.parse(line.slice(2)))
            } catch (parseError) {
              controller.error(parseError)
              return
            }
          }

          if (line.startsWith('3:')) {
            try {
              controller.error(new Error(JSON.parse(line.slice(2))))
            } catch (parseError) {
              controller.error(parseError)
            }
            return
          }
        }
      },
      flush(controller) {
        if (!buffer) {
          return
        }

        if (buffer.startsWith('0:')) {
          controller.enqueue(JSON.parse(buffer.slice(2)))
          return
        }

        if (buffer.startsWith('3:')) {
          controller.error(new Error(JSON.parse(buffer.slice(2))))
        }
      }
    }))
    .pipeThrough(new TextEncoderStream())
}

export async function POST(req) {
  try {
    const { userId, getToken } = await auth()
    if (!userId) {
      return new Response("Unauthorized", { status: 401 })
    }

    const body = await req.json()
    const { messages, reportId } = body
    const normalizedMessages = toBackendMessages(messages)

    if (!reportId) {
      return new Response("Missing reportId", { status: 400 })
    }

    if (normalizedMessages.length === 0) {
      return new Response("Missing messages", { status: 400 })
    }

    const token = await getToken()

    // Proxy request to FastAPI backend
    const response = await fetch(`http://127.0.0.1:8000/chat/${reportId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({ messages: normalizedMessages })
    })

    if (!response.ok) {
      const errorText = await response.text()
      console.error("FastAPI Chat Error:", errorText)
      return new Response(`Backend Error: ${response.status}`, { status: response.status })
    }

    const textStream = createLegacyProtocolTextStream(response.body)

    return new Response(textStream, {
      headers: {
        "Content-Type": "text/plain; charset=utf-8"
      }
    })
  } catch (error) {
    console.error("Chat API route error:", error)
    return new Response("Internal Server Error", { status: 500 })
  }
}
