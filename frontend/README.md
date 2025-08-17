# RAG Anything Assistant - Frontend

Modern frontend application built with Svelte + Vite for the RAG (Retrieval-Augmented Generation) Assistant.

## Features

### 🚀 Chat Interface
- **ChatGPT-like UI** with message bubbles
- **Real-time chat** with the RAG backend
- **Loading indicators** with typing animation
- **Source attribution** showing which documents were used
- **Example questions** to get started quickly

### 📊 Dashboard
- **Metrics cards** showing:
  - Total articles in knowledge base
  - Total GitHub projects cloned
  - Total conversations recorded

### 📜 History Viewer
- **Date picker** to select specific dates
- **Conversation table** showing all Q&A for selected date

## Technology Stack

- **Svelte** + **Vite** + **TypeScript**
- **Responsive design** with CSS Grid and Flexbox
- **Hash-based routing** for SPA navigation

## Getting Started

### Prerequisites
- Node.js 18+
- Backend server running on `http://localhost:8000`

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Open browser
# Navigate to http://localhost:5173
```

### Build for Production

```bash
npm run build
npm run preview
```

## Project Structure

```
src/
├── lib/
│   ├── api/backend.ts           # API client
│   ├── components/              # Reusable components
│   │   ├── ChatMessage.svelte
│   │   ├── ChatInput.svelte
│   │   ├── DashboardCard.svelte
│   │   └── HistoryTable.svelte
│   └── stores/                  # State management
│       ├── chatStore.ts
│       └── dashboardStore.ts
├── routes/                      # Page components
│   ├── +layout.svelte
│   ├── dashboard/+page.svelte
│   └── history/+page.svelte
└── App.svelte                   # Main app with routing
```

## Features in Detail

### Chat Interface
- Real-time messaging with RAG backend
- Loading states with typing animation
- Source attribution for responses
- Auto-scroll to latest messages
- Example questions to get started

### Dashboard
- Live metrics from backend API
- Colorful metric cards
- Loading states and error handling
- Responsive grid layout

### History Viewer
- Date picker for selecting chat history
- Conversation table with message details
- Source information for each response

## Configuration

Backend API URL can be changed in `src/lib/api/backend.ts`:

```typescript
const API_BASE_URL = 'http://localhost:8000';
```

## Contributing

1. Ensure backend is running on port 8000
2. Start frontend dev server: `npm run dev`
3. Make changes and test in browser
4. Build for production: `npm run build`

Built with ❤️ using Svelte + Vite
