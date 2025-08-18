'use client'

import { cn } from '@/lib/utils'
import { createClient } from '@/lib/supabase'
import { Button } from '@/components/ui/button'
import { 
  Card, 
  CardContent, 
  CardDescription, 
  CardHeader, 
  CardTitle 
} from '@/components/ui/card'
import { useState } from 'react'
import { Github } from 'lucide-react'

export function LoginForm({ className, ...props }: React.ComponentPropsWithoutRef<'div'>) {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleGithubLogin = async (e: React.MouseEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError(null)
    
    // Debug: Check if environment variables are loaded
    console.log('URL:', process.env.NEXT_PUBLIC_SUPABASE_URL)
    console.log('Key exists:', !!process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY)

    try {
      const supabase = createClient()
      const { error } = await supabase.auth.signInWithOAuth({
        provider: 'github',
        options: {
          redirectTo: `${window.location.origin}/auth/callback`,
          scopes: 'repo gist read:user user:email',
        },
      })

      if (error) {
        console.error('Auth error:', error)
        setError(error.message)
      }
    } catch (err) {
      console.error('Login error:', err)
      setError('Failed to sign in with GitHub. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Card className={cn('w-full', className)} {...props}>
      <CardHeader>
        <CardTitle>Welcome back</CardTitle>
        <CardDescription>
          Sign in to your account using your GitHub account
        </CardDescription>
      </CardHeader>
      <CardContent>
        {error && (
          <div className="mb-4 text-sm text-red-500">
            {error}
          </div>
        )}
        <Button 
          variant="outline" 
          className="w-full flex items-center gap-2" 
          onClick={handleGithubLogin}
          disabled={isLoading}
        >
          <Github size={20} />
          {isLoading ? 'Connecting...' : 'Continue with GitHub'}
        </Button>
      </CardContent>
    </Card>
  )
}
