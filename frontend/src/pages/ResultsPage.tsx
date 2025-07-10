import { useParams } from 'react-router-dom'
import { useQuery } from 'react-query'
import { useState } from 'react'
import { motion } from 'framer-motion'
import { ExternalLink, Users, Calendar, Quote, Trophy, TrendingUp, Filter } from 'lucide-react'
import { searchAPI } from '../services/api'
import CitationChart from '../components/CitationChart'

const ResultsPage = () => {
  const { searchId } = useParams<{ searchId: string }>()
  const [filterYear, setFilterYear] = useState<number | null>(null)
  const [filterMinCitations, setFilterMinCitations] = useState<number>(0)
  
  const { data: search, isLoading } = useQuery(
    ['searchDetails', searchId],
    () => searchAPI.getSearchDetails(parseInt(searchId!)),
    { enabled: !!searchId }
  )

  if (isLoading || !search) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  const filteredArticles = search.articles?.filter(article => {
    if (filterYear && article.year !== filterYear) return false
    if (article.citations < filterMinCitations) return false
    return true
  }) || []

  const yearOptions = [...new Set(search.articles?.map(a => a.year).filter(Boolean))].sort((a, b) => b! - a!)

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Results for "{search.keyword}"
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Found {search.total_results} articles
        </p>
      </div>

      {search.articles && search.articles.length > 0 && (
        <div className="mb-8">
          <CitationChart articles={search.articles} />
        </div>
      )}

      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4 mb-6">
        <div className="flex items-center space-x-4">
          <Filter className="h-5 w-5 text-gray-600 dark:text-gray-400" />
          
          <select
            value={filterYear || ''}
            onChange={(e) => setFilterYear(e.target.value ? parseInt(e.target.value) : null)}
            className="px-3 py-1 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-sm"
          >
            <option value="">All Years</option>
            {yearOptions.map(year => (
              <option key={year} value={year}>{year}</option>
            ))}
          </select>
          
          <div className="flex items-center space-x-2">
            <label className="text-sm text-gray-600 dark:text-gray-400">
              Min Citations:
            </label>
            <input
              type="number"
              min="0"
              value={filterMinCitations}
              onChange={(e) => setFilterMinCitations(parseInt(e.target.value) || 0)}
              className="w-20 px-2 py-1 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-sm"
            />
          </div>
          
          <span className="text-sm text-gray-600 dark:text-gray-400 ml-auto">
            Showing {filteredArticles.length} of {search.articles?.length || 0} articles
          </span>
        </div>
      </div>

      <div className="space-y-4">
        {filteredArticles.map((article, index) => (
          <motion.article
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.05 }}
            className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
          >
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              {article.url ? (
                <a
                  href={article.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-primary-600 transition-colors flex items-center"
                >
                  {article.title}
                  <ExternalLink className="h-4 w-4 ml-2" />
                </a>
              ) : (
                article.title
              )}
            </h3>

            <div className="flex flex-wrap gap-4 text-sm text-gray-600 dark:text-gray-400 mb-3">
              {article.authors && (
                <span className="flex items-center">
                  <Users className="h-4 w-4 mr-1" />
                  {article.authors}
                </span>
              )}
              
              {article.year && (
                <span className="flex items-center">
                  <Calendar className="h-4 w-4 mr-1" />
                  {article.year}
                </span>
              )}
              
              {article.venue && (
                <span>{article.venue}</span>
              )}
              
              {article.publisher && (
                <span>{article.publisher}</span>
              )}
            </div>

            {article.description && (
              <p className="text-gray-700 dark:text-gray-300 mb-3 line-clamp-3">
                <Quote className="inline h-4 w-4 mr-1" />
                {article.description}
              </p>
            )}

            <div className="flex items-center space-x-4 text-sm">
              <span className="flex items-center text-primary-600 dark:text-primary-400 font-medium">
                <Trophy className="h-4 w-4 mr-1" />
                {article.citations} citations
              </span>
              
              {article.citations_per_year > 0 && (
                <span className="flex items-center text-green-600 dark:text-green-400 font-medium">
                  <TrendingUp className="h-4 w-4 mr-1" />
                  {article.citations_per_year.toFixed(1)}/year
                </span>
              )}
            </div>
          </motion.article>
        ))}
      </div>
    </div>
  )
}

export default ResultsPage