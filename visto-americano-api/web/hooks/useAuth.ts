"use client";

import { useEffect, useState } from "react";
import type { User } from "@/types/User";

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const API = process.env.NEXT_PUBLIC_API_URL;

  async function load() {
  try {
    const token = localStorage.getItem("token");

    if (!token) {
      setUser(null);
      setLoading(false);
      return;
    }

    const res = await fetch(`${API}/usuarios/me`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (res.ok) {
      const data: User = await res.json();
      setUser(data);
    } else {
      setUser(null);
    }
  } catch (error) {
    setUser(null);
  } finally {
    setLoading(false);
  }
}

  useEffect(() => {
    load();
  }, []);

  return { user, loading };
}