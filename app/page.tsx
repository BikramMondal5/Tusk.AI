"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Progress } from "@/components/ui/progress"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import {
  Play,
  Download,
  Share2,
  Facebook,
  Twitter,
  MessageCircle,
  Loader2,
  Youtube,
  Globe,
  History,
  Sparkles,
} from "lucide-react"
import { Header } from "@/components/header"
import { Footer } from "@/components/footer"

const languages = [
  { code: "en", name: "English", flag: "🇺🇸" },
  { code: "hi", name: "Hindi", flag: "🇮🇳" },
  { code: "es", name: "Spanish", flag: "🇪🇸" },
  { code: "fr", name: "French", flag: "🇫🇷" },
  { code: "de", name: "German", flag: "🇩🇪" },
  { code: "ja", name: "Japanese", flag: "🇯🇵" },
  { code: "zh", name: "Chinese", flag: "🇨🇳" },
  { code: "bn", name: "Bengali", flag: "🇧🇩" },
  { code: "ar", name: "Arabic", flag: "🇸🇦" },
  { code: "ru", name: "Russian", flag: "🇷🇺" },
  { code: "pt", name: "Portuguese", flag: "🇧🇷" },
  { code: "ko", name: "Korean", flag: "🇰🇷" },
]

const mockHistory = [
  {
    id: 1,
    title: "Tech Tutorial - Python Basics",
    originalLang: "English",
    dubbedLang: "Spanish",
    date: "2024-01-15",
    thumbnail: "/placeholder.svg?height=120&width=200",
  },
  {
    id: 2,
    title: "Cooking Recipe - Italian Pasta",
    originalLang: "Italian",
    dubbedLang: "Hindi",
    date: "2024-01-14",
    thumbnail: "/placeholder.svg?height=120&width=200",
  },
  {
    id: 3,
    title: "Music Video - Pop Song",
    originalLang: "English",
    dubbedLang: "French",
    date: "2024-01-13",
    thumbnail: "/placeholder.svg?height=120&width=200",
  },
]

export default function TusiAI() {
  const [youtubeUrl, setYoutubeUrl] = useState("")
  const [selectedLanguage, setSelectedLanguage] = useState("")
  const [isProcessing, setIsProcessing] = useState(false)
  const [progress, setProgress] = useState(0)
  const [showResult, setShowResult] = useState(false)
  const [showHistory, setShowHistory] = useState(false)
  // Add this to handle client-side only rendering
  const [isClient, setIsClient] = useState(false)

  // This effect runs only on the client after hydration is complete
  useEffect(() => {
    setIsClient(true)
  }, [])

  const handleDubbing = async () => {
    if (!youtubeUrl || !selectedLanguage) return

    setIsProcessing(true)
    setProgress(0)
    setShowResult(false)

    try {
      // Call our API endpoint to fetch the transcript
      const response = await fetch('/api/transcript', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ videoUrl: youtubeUrl }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        console.error('Error fetching transcript:', errorData.error);
        throw new Error(errorData.error || 'Failed to fetch transcript');
      }

      const data = await response.json();
      console.log('Transcript data:', data.transcript);
      
      // Simulate processing with progress updates
      const progressInterval = setInterval(() => {
        setProgress((prev) => {
          if (prev >= 100) {
            clearInterval(progressInterval)
            setIsProcessing(false)
            setShowResult(true)
            return 100
          }
          return prev + Math.random() * 15
        })
      }, 500)
    } catch (error) {
      console.error('Error in handleDubbing:', error);
      setIsProcessing(false);
      // You could set an error state here to show to the user
    }
  }

  const isValidYouTubeUrl = (url: string) => {
    const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+/
    return youtubeRegex.test(url)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 dark:from-slate-900 dark:to-slate-800">
      <Header />

      <main className="container mx-auto px-4 py-8">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center gap-2 mb-4">
            <Sparkles className="h-8 w-8 text-blue-600" />
            <h1 className="text-4xl md:text-6xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              tusi.ai
            </h1>
          </div>
          <p className="text-xl text-slate-600 dark:text-slate-300 max-w-2xl mx-auto">
            Dub any video in any language with AI. Transform your content for global audiences in minutes.
          </p>
        </div>

        {/* Main Dubbing Interface */}
        <div className="max-w-4xl mx-auto mb-16">
          <Card className="shadow-xl border-0 bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-2xl">
                <Youtube className="h-6 w-6 text-red-500" />
                Create Your Dub
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* YouTube URL Input */}
              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-700 dark:text-slate-300">YouTube Video URL</label>
                <Input
                  type="url"
                  placeholder="Paste your YouTube link here..."
                  value={youtubeUrl}
                  onChange={(e) => setYoutubeUrl(e.target.value)}
                  className="h-12 text-lg transition-all duration-200 focus:ring-2 focus:ring-blue-500"
                />
                {youtubeUrl && !isValidYouTubeUrl(youtubeUrl) && (
                  <p className="text-sm text-red-500">Please enter a valid YouTube URL</p>
                )}
              </div>

              {/* Language Selector - Only render when client-side */}
              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-700 dark:text-slate-300 flex items-center gap-2">
                  <Globe className="h-4 w-4" />
                  Target Language
                </label>
                {isClient ? (
                  <Select value={selectedLanguage} onValueChange={setSelectedLanguage}>
                    <SelectTrigger className="h-12 text-lg">
                      <SelectValue placeholder="Select target language" />
                    </SelectTrigger>
                    <SelectContent>
                      {languages.map((lang) => (
                        <SelectItem key={lang.code} value={lang.code}>
                          <div className="flex items-center gap-2">
                            <span className="text-lg">{lang.flag}</span>
                            <span>{lang.name}</span>
                          </div>
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                ) : (
                  <div className="h-12 border rounded-md flex items-center px-3 text-muted-foreground">
                    Loading languages...
                  </div>
                )}
              </div>

              {/* Dub Button */}
              <Button
                onClick={handleDubbing}
                disabled={!youtubeUrl || !selectedLanguage || !isValidYouTubeUrl(youtubeUrl) || isProcessing}
                className="w-full h-14 text-lg font-semibold bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 transition-all duration-200 transform hover:scale-[1.02]"
              >
                {isProcessing ? (
                  <>
                    <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                    Processing...
                  </>
                ) : (
                  <>
                    <Sparkles className="mr-2 h-5 w-5" />
                    Dub Now
                  </>
                )}
              </Button>

              {/* Progress Bar */}
              {isProcessing && (
                <div className="space-y-2">
                  <div className="flex justify-between text-sm text-slate-600 dark:text-slate-400">
                    <span>Processing your video...</span>
                    <span>{Math.round(progress)}%</span>
                  </div>
                  <Progress value={progress} className="h-2" />
                </div>
              )}

              {/* Result Section */}
              {showResult && (
                <div className="space-y-4 p-6 bg-gradient-to-r from-green-50 to-blue-50 dark:from-green-900/20 dark:to-blue-900/20 rounded-lg border border-green-200 dark:border-green-800">
                  <div className="flex items-center gap-2 text-green-700 dark:text-green-400">
                    <Sparkles className="h-5 w-5" />
                    <span className="font-semibold">Dubbing Complete!</span>
                  </div>

                  {/* Video Player Placeholder */}
                  <div className="relative bg-black rounded-lg overflow-hidden">
                    <div className="aspect-video flex items-center justify-center">
                      <div className="text-center text-white">
                        <Play className="h-16 w-16 mx-auto mb-2 opacity-80" />
                        <p className="text-lg">Dubbed Video Preview</p>
                        <p className="text-sm opacity-70">Click to play your dubbed video</p>
                      </div>
                    </div>
                  </div>

                  {/* Action Buttons */}
                  <div className="flex flex-wrap gap-3">
                    <Button className="flex-1 min-w-[140px]">
                      <Download className="mr-2 h-4 w-4" />
                      Download
                    </Button>
                    <Button variant="outline" className="flex-1 min-w-[140px]">
                      <Share2 className="mr-2 h-4 w-4" />
                      Share
                    </Button>
                    <div className="flex gap-2">
                      <Button size="icon" variant="outline" className="text-blue-600">
                        <Facebook className="h-4 w-4" />
                      </Button>
                      <Button size="icon" variant="outline" className="text-sky-500">
                        <Twitter className="h-4 w-4" />
                      </Button>
                      <Button size="icon" variant="outline" className="text-green-600">
                        <MessageCircle className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* History Section */}
        <div className="max-w-4xl mx-auto">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold flex items-center gap-2">
              <History className="h-6 w-6 text-blue-600" />
              Recent Dubs
            </h2>
            <Button
              variant="outline"
              onClick={() => setShowHistory(!showHistory)}
              className="transition-all duration-200"
            >
              {showHistory ? "Hide" : "Show"} History
            </Button>
          </div>

          {showHistory && (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {mockHistory.map((item) => (
                <Card key={item.id} className="group hover:shadow-lg transition-all duration-200 cursor-pointer">
                  <CardContent className="p-4">
                    <div className="aspect-video bg-slate-200 dark:bg-slate-700 rounded-lg mb-3 overflow-hidden">
                      <img
                        src={item.thumbnail || "/placeholder.svg"}
                        alt={item.title}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-200"
                      />
                    </div>
                    <h3 className="font-semibold text-sm mb-2 line-clamp-2">{item.title}</h3>
                    <div className="flex gap-2 mb-2">
                      <Badge variant="secondary" className="text-xs">
                        {item.originalLang} → {item.dubbedLang}
                      </Badge>
                    </div>
                    <p className="text-xs text-slate-500 dark:text-slate-400">{item.date}</p>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>
      </main>

      <Footer />
    </div>
  )
}
