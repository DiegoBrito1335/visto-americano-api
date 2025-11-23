"use client";

import Link from "next/link";
import { useEffect } from "react";
import { Button } from "@/components/ui/button";
import { NavigationMenu, NavigationMenuItem, NavigationMenuList } from "@/components/ui/navigation-menu";
import { useAuth } from "@/lib/auth";

export function Navbar() {
  const { user, logout } = useAuth();

  return (
    <header className="border-b bg-background/70 backdrop-blur-md sticky top-0 z-50">
      <div className="container mx-auto flex items-center justify-between py-4 px-2">
        <Link href="/" className="text-2xl font-bold">
          🇺🇸 VistoAmericano
        </Link>

        <NavigationMenu>
          <NavigationMenuList className="flex gap-6">
            <NavigationMenuItem>
              <Link href="/ds160" className="text-sm hover:underline">
                DS-160
              </Link>
            </NavigationMenuItem>

            <NavigationMenuItem>
              <Link href="/entrevista" className="text-sm hover:underline">
                Entrevista
              </Link>
            </NavigationMenuItem>

            <NavigationMenuItem>
              <Link href="/dashboard" className="text-sm hover:underline">
                Dashboard
              </Link>
            </NavigationMenuItem>
          </NavigationMenuList>
        </NavigationMenu>

        <div>
          {user ? (
            <div className="flex items-center gap-3">
              <span className="text-sm">{user.email}</span>
              <Button variant="destructive" onClick={() => { logout(); window.location.href = "/"; }}>
                Sair
              </Button>
            </div>
          ) : (
            <Link href="/login">
              <Button>Entrar</Button>
            </Link>
          )}
        </div>
      </div>
    </header>
  );
}
