import { useQuery, useMutation, useQueryClient } from 'react-query'
import { Link } from 'react-router-dom'
import { format } from 'date-fns'
import { motion } from 'framer-motion'
import { Trash2, Eye, Download, Calendar, FileText, Search } from 'lucide-react'
import toast from 'react-hot-toast'
import { searchAPI } from '../services/api'

const HistoryPage = () => {
  const queryClient = useQueryClient()
  
  const { data: searches, isLoading } = useQuery(
    'searchHistory',
    () => searchAPI.getSearchHistory(0, 50)
  )

  const deleteMutation = useMutation(searchAPI.deleteSearch, {
    onSuccess: () => {
      queryClient.invalidateQueries('searchHistory')
      toast.success('Search deleted successfully')
    },
    onError: () => {
      toast.error('Failed to delete search')
    },
  })

  const handleExport = async (searchId: number, format: string) => {
    try {
      const blob = await searchAPI.exportResults(searchId, format)
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `scholar_results_${searchId}.${format}`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      toast.success(`Exported as ${format.toUpperCase()}`)
    } catch (error) {
      toast.error('Export failed')
    }
  }

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Search History
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          View and manage your previous searches
        </p>
      </div>

      {searches && searches.length > 0 ? (
        <div className="space-y-4">
          {searches.map((search, index) => (
            <motion.div
              key={search.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05 }}
              className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
            >
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                    <Search className="inline h-4 w-4 mr-2" />
                    {search.keyword}
                  </h3>
                  
                  <div className="flex flex-wrap gap-4 text-sm text-gray-600 dark:text-gray-400">
                    <span className="flex items-center">
                      <Calendar className="h-4 w-4 mr-1" />
                      {format(new Date(search.created_at), 'PPP')}
                    </span>
                    <span className="flex items-center">
                      <FileText className="h-4 w-4 mr-1" />
                      {search.total_results} results
                    </span>
                    {search.start_year && search.end_year && (
                      <span>
                        Year: {search.start_year} - {search.end_year}
                      </span>
                    )}
                  </div>
                </div>

                <div className="flex space-x-2 ml-4">
                  <Link
                    to={`/results/${search.id}`}
                    className="p-2 text-primary-600 hover:bg-primary-50 dark:hover:bg-gray-700 rounded-lg transition-colors"
                    title="View Results"
                  >
                    <Eye className="h-5 w-5" />
                  </Link>
                  
                  <div className="relative group">
                    <button
                      className="p-2 text-green-600 hover:bg-green-50 dark:hover:bg-gray-700 rounded-lg transition-colors"
                      title="Export"
                    >
                      <Download className="h-5 w-5" />
                    </button>
                    <div className="absolute right-0 mt-2 w-32 bg-white dark:bg-gray-700 rounded-lg shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-10">
                      <button
                        onClick={() => handleExport(search.id, 'csv')}
                        className="block w-full text-left px-4 py-2 text-sm hover:bg-gray-100 dark:hover:bg-gray-600 rounded-t-lg"
                      >
                        CSV
                      </button>
                      <button
                        onClick={() => handleExport(search.id, 'json')}
                        className="block w-full text-left px-4 py-2 text-sm hover:bg-gray-100 dark:hover:bg-gray-600"
                      >
                        JSON
                      </button>
                      <button
                        onClick={() => handleExport(search.id, 'excel')}
                        className="block w-full text-left px-4 py-2 text-sm hover:bg-gray-100 dark:hover:bg-gray-600"
                      >
                        Excel
                      </button>
                      <button
                        onClick={() => handleExport(search.id, 'bibtex')}
                        className="block w-full text-left px-4 py-2 text-sm hover:bg-gray-100 dark:hover:bg-gray-600 rounded-b-lg"
                      >
                        BibTeX
                      </button>
                    </div>
                  </div>
                  
                  <button
                    onClick={() => deleteMutation.mutate(search.id)}
                    className="p-2 text-red-600 hover:bg-red-50 dark:hover:bg-gray-700 rounded-lg transition-colors"
                    title="Delete"
                  >
                    <Trash2 className="h-5 w-5" />
                  </button>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <Search className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600 dark:text-gray-400">No search history yet</p>
          <Link
            to="/"
            className="mt-4 inline-block text-primary-600 hover:text-primary-700 font-medium"
          >
            Start your first search
          </Link>
        </div>
      )}
    </div>
  )
}

export default HistoryPage