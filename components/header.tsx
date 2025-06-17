"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { ThemeToggle } from "@/components/theme-toggle"
import { Menu, X, Sparkles } from "lucide-react"

export function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const [mounted, setMounted] = useState(false)

  // Only render interactive elements on the client to avoid hydration mismatch
  useEffect(() => {
    setMounted(true)
  }, [])

  const navItems = [
    { name: "Home", href: "#" },
    { name: "How It Works", href: "#" },
    { name: "About", href: "#" },
    { name: "Contact", href: "#" },
  ]

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm">
      <div className="container mx-auto px-4">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <div className="flex items-center gap-2">
            <Sparkles className="h-6 w-6 text-blue-600" />
            <span className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              tusi.ai
            </span>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-6">
            {navItems.map((item) => (
              <a
                key={item.name}
                href={item.href}
                className="text-sm font-medium text-slate-600 hover:text-blue-600 dark:text-slate-300 dark:hover:text-blue-400 transition-colors"
              >
                {item.name}
              </a>
            ))}
          </nav>

          {/* Right Side */}
          <div className="flex items-center gap-4">
            <ThemeToggle />
            
            {/* Desktop Auth Buttons - Client Only */}
            <div className="hidden md:flex items-center gap-2">
              {mounted ? (
                <>
                  <Button variant="ghost" size="sm">
                    Login
                  </Button>
                  <Button size="sm" className="bg-blue-600 hover:bg-blue-700">
                    Register
                  </Button>
                </>
              ) : (
                <>
                  <div className="w-16 h-9 rounded-md border border-transparent"></div>
                  <div className="w-20 h-9 rounded-md bg-blue-600"></div>
                </>
              )}
            </div>

            {/* Mobile Menu Button - Client Only */}
            {mounted ? (
              <Button variant="ghost" size="icon" className="md:hidden" onClick={() => setIsMenuOpen(!isMenuOpen)}>
                {isMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
              </Button>
            ) : (
              <div className="w-9 h-9 md:hidden"></div>
            )}
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && mounted && (
          <div className="md:hidden border-t bg-white dark:bg-slate-900 py-4">
            <nav className="flex flex-col gap-4">
              {navItems.map((item) => (
                <a
                  key={item.name}
                  href={item.href}
                  className="text-sm font-medium text-slate-600 hover:text-blue-600 dark:text-slate-300 dark:hover:text-blue-400 transition-colors"
                  onClick={() => setIsMenuOpen(false)}
                >
                  {item.name}
                </a>
              ))}
              <div className="flex gap-2 pt-2 border-t">
                <Button variant="ghost" size="sm" className="flex-1">
                  Login
                </Button>
                <Button size="sm" className="flex-1 bg-blue-600 hover:bg-blue-700">
                  Register
                </Button>
              </div>
            </nav>
          </div>
        )}
      </div>
    </header>
  )
}
