import { NextResponse } from "next/server";
import { auth } from '@clerk/nextjs/server'

export async function GET() {
  try {
    const { getToken } = await auth();
    const token = await getToken();
    
    if (!token) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    const backendUrl = process.env.PYTHON_BACKEND_URL || "http://localhost:8000";
    
    const response = await fetch(`${backendUrl}/reports`, {
      headers: {
        "Authorization": `Bearer ${token}`
      }
    });

    if (!response.ok) {
      return NextResponse.json({ error: `Backend responded with ${response.status}` }, { status: response.status });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error("API Route error:", error);
    return NextResponse.json({ error: "Internal server error" }, { status: 500 });
  }
}
