"use client";

import { useEffect, useState } from "react";
import type { User } from "@/types/User";

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const API = process.env.NEXT_PUBLIC_API_URL;

  useEffect(() => {
    let isMounted = true; // Previne updates após unmount
    
    async function load() {
      try {
        const res = await fetch(`${API}/usuarios/me`, {
          credentials: "include",
        });
        
        if (res.ok && isMounted) {
          const data: User = await res.json();
          setUser(data);
        } else if (isMounted) {
          setUser(null);
        }
      } catch (error) {
        if (isMounted) {
          setUser(null);
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    }

    load();
    
    return () => {
      isMounted = false; // Cleanup
    };
  }, [API]); // Adiciona API como dependência

  return { user, loading };
}