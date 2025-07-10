import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from 'react-query'
import { Toaster } from 'react-hot-toast'
import Layout from './components/Layout'
import SearchPage from './pages/SearchPage'
import HistoryPage from './pages/HistoryPage'
import ResultsPage from './pages/ResultsPage'
import { ThemeProvider } from './contexts/ThemeContext'

const queryClient = new QueryClient()

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <Router>
          <Layout>
            <Routes>
              <Route path="/" element={<SearchPage />} />
              <Route path="/history" element={<HistoryPage />} />
              <Route path="/results/:searchId" element={<ResultsPage />} />
            </Routes>
          </Layout>
          <Toaster position="top-right" />
        </Router>
      </ThemeProvider>
    </QueryClientProvider>
  )
}

export default App