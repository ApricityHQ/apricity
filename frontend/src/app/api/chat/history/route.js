import { auth } from '@clerk/nextjs/server'

function toUiMessage(message) {
  return {
    id: message.id,
    role: message.role,
    parts: [
      {
        type: 'text',
        text: message.content || ''
      }
    ]
  }
}

export async function GET(req) {
  try {
    const { userId, getToken } = await auth()
    if (!userId) return new Response("Unauthorized", { status: 401 })
    
    const { searchParams } = new URL(req.url)
    const reportId = searchParams.get('reportId')
    
    if (!reportId) return new Response("Missing reportId", { status: 400 })
    
    const token = await getToken()
    
    const res = await fetch(`http://127.0.0.1:8000/chat/${reportId}`, {
      headers: { "Authorization": `Bearer ${token}` }
    })
    
    if (!res.ok) return new Response(`Backend Error: ${res.status}`, { status: res.status })
    
    const data = await res.json()
    return new Response(JSON.stringify((data.messages || []).map(toUiMessage)), {
      headers: { "Content-Type": "application/json" }
    })
  } catch (error) {
    console.error("Chat history error:", error)
    return new Response("Internal Server Error", { status: 500 })
  }
}
