import { NextResponse } from "next/server";

export async function POST(req: Request) {
  const body = await req.json();

  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify(body),
  });

  const data = await res.json();

  const response = NextResponse.json(data, { status: res.status });

  const cookie = res.headers.get("set-cookie");
  if (cookie) response.headers.set("set-cookie", cookie);

  return response;
}
