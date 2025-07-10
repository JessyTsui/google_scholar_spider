import { useEffect, useRef } from 'react'
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
  ChartOptions,
} from 'chart.js'
import { Chart } from 'react-chartjs-2'
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
  const chartRef = useRef<ChartJS>(null)

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
        type: 'bar' as const,
        label: 'Total Citations',
        data: sortedYears.map(year => yearCitations[year]),
        backgroundColor: 'rgba(14, 165, 233, 0.5)',
        borderColor: 'rgb(14, 165, 233)',
        borderWidth: 1,
      },
      {
        type: 'line' as const,
        label: 'Articles Published',
        data: sortedYears.map(year => 
          articles.filter(a => a.year === year).length
        ),
        borderColor: 'rgb(34, 197, 94)',
        backgroundColor: 'rgba(34, 197, 94, 0.5)',
        yAxisID: 'y1',
      }
    ],
  }

  const options: ChartOptions<'bar'> = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Citations and Publications by Year',
      },
    },
    scales: {
      y: {
        type: 'linear' as const,
        display: true,
        position: 'left' as const,
        title: {
          display: true,
          text: 'Citations',
        },
      },
      y1: {
        type: 'linear' as const,
        display: true,
        position: 'right' as const,
        grid: {
          drawOnChartArea: false,
        },
        title: {
          display: true,
          text: 'Articles',
        },
      },
    },
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
      <Chart ref={chartRef} type='bar' data={data} options={options} />
    </div>
  )
}

export default CitationChart