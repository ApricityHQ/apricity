import { auth } from '@clerk/nextjs/server'

export async function POST(req) {
  try {
    const { userId, getToken } = await auth()
    if (!userId) {
      return new Response("Unauthorized", { status: 401 })
    }

    const body = await req.json()
    const { messages, reportId } = body

    if (!reportId) {
      return new Response("Missing reportId", { status: 400 })
    }

    const token = await getToken()

    // Proxy request to FastAPI backend
    const response = await fetch(`http://127.0.0.1:8000/chat/${reportId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({ messages })
    })

    if (!response.ok) {
      const errorText = await response.text()
      console.error("FastAPI Chat Error:", errorText)
      return new Response(`Backend Error: ${response.status}`, { status: response.status })
    }

    // Proxy the raw Data Stream back to Vercel AI SDK useChat
    return new Response(response.body, {
      headers: {
        "Content-Type": "text/plain; charset=utf-8",
        "Transfer-Encoding": "chunked",
      }
    })
  } catch (error) {
    console.error("Chat API route error:", error)
    return new Response("Internal Server Error", { status: 500 })
  }
}
