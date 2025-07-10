import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'
import { Bar } from 'react-chartjs-2'
import { Article } from '../services/api'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
)

interface CitationChartProps {
  articles: Article[]
}

const CitationChart = ({ articles }: CitationChartProps) => {

  const yearCitations = articles.reduce((acc, article) => {
    if (article.year) {
      acc[article.year] = (acc[article.year] || 0) + article.citations
    }
    return acc
  }, {} as Record<number, number>)

  const sortedYears = Object.keys(yearCitations).map(Number).sort()
  
  const data = {
    labels: sortedYears.map(String),
    datasets: [
      {
        label: 'Total Citations',
        data: sortedYears.map(year => yearCitations[year]),
        backgroundColor: 'rgba(14, 165, 233, 0.5)',
        borderColor: 'rgb(14, 165, 233)',
        borderWidth: 1,
      }
    ],
  }

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Citations by Year',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Citations',
        },
      },
    },
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
      <Bar data={data} options={options} />
    </div>
  )
}

export default CitationChart