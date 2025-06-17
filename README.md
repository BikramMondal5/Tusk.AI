# Auto-Dub

A Next.js application that uses AI to automatically dub YouTube videos into different languages.

## Features

- Extract YouTube video transcripts automatically
- Translate and dub videos into multiple languages
- User-friendly interface with real-time progress tracking
- History of previously dubbed videos
- Dark mode support
- Responsive design for mobile and desktop

## Tech Stack

- **Frontend**: Next.js 14, React, TypeScript, Tailwind CSS
- **UI Components**: Shadcn UI library
- **API**: Next.js API routes
- **Styling**: Tailwind CSS with custom theming
- **Icons**: Lucide React

## Getting Started

### Prerequisites

- Node.js (v18.0.0 or higher)
- npm or pnpm

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/auto-dub.git
cd auto-dub
```

2. Install dependencies:
```bash
npm install
# or
pnpm install
```

3. Run the development server:
```bash
npm run dev
# or
pnpm dev
```

4. Open [http://localhost:3000](http://localhost:3000) with your browser to see the application.

## Project Structure

- `app/` - Next.js app directory
  - `api/` - API routes including transcript extraction
  - `page.tsx` - Main application page
  - `layout.tsx` - Root layout with theme provider
  - `globals.css` - Global styles and theme variables
- `components/` - Reusable UI components
  - `ui/` - Shadcn UI components
  - `header.tsx` - Application header with navigation
  - `footer.tsx` - Application footer
  - `theme-toggle.tsx` - Dark/light mode toggle
- `public/` - Static assets

## Environment Variables

Create a `.env.local` file in the root directory with the following variables:

```
# Add your environment variables here
# For example: API keys for translation services
```

## Features in Detail

### YouTube Video Processing

1. User inputs a YouTube video URL
2. App extracts the video ID and fetches the transcript using the YouTube Transcript API
3. The transcript is then processed and translated to the target language
4. Audio dubbing is generated using AI TTS services
5. The result is a dubbed version of the original video

### Supported Languages

The application supports dubbing into multiple languages including but not limited to:
- English
- Spanish
- French
- German
- Japanese
- Chinese
- Hindi
- Bengali
- Arabic
- Russian
- Portuguese
- Korean

## Contribution

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT](LICENSE)