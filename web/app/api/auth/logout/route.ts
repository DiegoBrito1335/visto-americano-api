import { NextResponse } from "next/server";

export async function POST() {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/logout`, {
    method: "POST",
    credentials: "include",
  });

  const data = await res.json();

  const response = NextResponse.json(data, { status: 200 });

  response.headers.set(
    "Set-Cookie",
    "token=; Path=/; HttpOnly; Max-Age=0"
  );

  return response;
}
