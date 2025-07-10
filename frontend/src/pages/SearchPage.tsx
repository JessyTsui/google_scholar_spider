import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useMutation } from 'react-query'
import { motion } from 'framer-motion'
import { Search, Loader2, Calendar, SortDesc, FileText } from 'lucide-react'
import toast from 'react-hot-toast'
import { searchAPI, SearchRequest } from '../services/api'

const SearchPage = () => {
  const navigate = useNavigate()
  const currentYear = new Date().getFullYear()
  
  const [formData, setFormData] = useState<SearchRequest>({
    keyword: '',
    num_results: 50,
    sort_by: 'citations',
    start_year: undefined,
    end_year: undefined,
  })

  const searchMutation = useMutation(searchAPI.search, {
    onSuccess: (data) => {
      toast.success(`Found ${data.total_results} articles`)
      navigate(`/results/${data.search_id}`)
    },
    onError: () => {
      toast.error('Search failed. Please try again.')
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!formData.keyword.trim()) {
      toast.error('Please enter a search keyword')
      return
    }
    searchMutation.mutate(formData)
  }

  return (
    <div className="max-w-4xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-12"
      >
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
          Google Scholar Spider
        </h1>
        <p className="text-lg text-gray-600 dark:text-gray-400">
          Search and analyze academic articles with ease
        </p>
      </motion.div>

      <motion.form
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
        onSubmit={handleSubmit}
        className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8"
      >
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Search Keywords
            </label>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                value={formData.keyword}
                onChange={(e) => setFormData({ ...formData, keyword: e.target.value })}
                placeholder="e.g., machine learning, artificial intelligence"
                className="w-full pl-10 pr-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                <FileText className="inline h-4 w-4 mr-1" />
                Number of Results
              </label>
              <select
                value={formData.num_results}
                onChange={(e) => setFormData({ ...formData, num_results: parseInt(e.target.value) })}
                className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              >
                <option value={10}>10</option>
                <option value={20}>20</option>
                <option value={50}>50</option>
                <option value={100}>100</option>
                <option value={200}>200</option>
                <option value={500}>500</option>
                <option value={1000}>1000</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                <Calendar className="inline h-4 w-4 mr-1" />
                Start Year
              </label>
              <input
                type="number"
                min="1900"
                max={currentYear}
                value={formData.start_year || ''}
                onChange={(e) => setFormData({ ...formData, start_year: e.target.value ? parseInt(e.target.value) : undefined })}
                placeholder="Optional"
                className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                <Calendar className="inline h-4 w-4 mr-1" />
                End Year
              </label>
              <input
                type="number"
                min="1900"
                max={currentYear}
                value={formData.end_year || ''}
                onChange={(e) => setFormData({ ...formData, end_year: e.target.value ? parseInt(e.target.value) : undefined })}
                placeholder="Optional"
                className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              <SortDesc className="inline h-4 w-4 mr-1" />
              Sort By
            </label>
            <select
              value={formData.sort_by}
              onChange={(e) => setFormData({ ...formData, sort_by: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            >
              <option value="citations">Total Citations</option>
              <option value="citations_per_year">Citations per Year</option>
              <option value="year">Publication Year</option>
            </select>
          </div>

          <button
            type="submit"
            disabled={searchMutation.isLoading}
            className="w-full py-3 px-4 bg-primary-600 hover:bg-primary-700 text-white font-medium rounded-lg transition-colors duration-200 flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {searchMutation.isLoading ? (
              <>
                <Loader2 className="h-5 w-5 animate-spin" />
                <span>Searching...</span>
              </>
            ) : (
              <>
                <Search className="h-5 w-5" />
                <span>Search Google Scholar</span>
              </>
            )}
          </button>
        </div>
      </motion.form>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
        className="mt-8 text-center text-sm text-gray-600 dark:text-gray-400"
      >
        <p>This tool is for educational purposes only.</p>
        <p>Please respect Google Scholar's terms of service.</p>
      </motion.div>
    </div>
  )
}

export default SearchPage