import React from 'react';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell,
} from 'recharts';

interface ChartData {
  series?: Array<Record<string, unknown>>;
  xKey?: string;
  yKey?: string;
}

interface DynamicChartProps {
  type: 'bar_chart' | 'line_chart' | 'radar_chart' | 'pie_chart' | 'table';
  data: ChartData;
  title?: string;
}

const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899', '#06B6D4', '#84CC16'];

export const DynamicChart: React.FC<DynamicChartProps> = ({ type, data, title }) => {
  const series = data.series || [];
  const xKey = data.xKey || 'name';
  const yKey = data.yKey || 'value';

  if (series.length === 0) {
    return <p className="text-gray-500 text-center py-4">Nessun dato disponibile</p>;
  }

  const renderChart = () => {
    switch (type) {
      case 'bar_chart':
        return (
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={series} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
              <XAxis dataKey={xKey} tick={{ fontSize: 12 }} />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip
                contentStyle={{ backgroundColor: '#fff', border: '1px solid #E5E7EB', borderRadius: '8px' }}
              />
              <Legend />
              <Bar dataKey={yKey} radius={[4, 4, 0, 0]}>
                {series.map((_, index) => (
                  <Cell key={index} fill={COLORS[index % COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        );

      case 'line_chart':
        return (
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={series} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
              <XAxis dataKey={xKey} tick={{ fontSize: 12 }} />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip
                contentStyle={{ backgroundColor: '#fff', border: '1px solid #E5E7EB', borderRadius: '8px' }}
              />
              <Legend />
              <Line
                type="monotone"
                dataKey={yKey}
                stroke="#3B82F6"
                strokeWidth={2}
                dot={{ fill: '#3B82F6', r: 4 }}
                activeDot={{ r: 6 }}
              />
            </LineChart>
          </ResponsiveContainer>
        );

      case 'pie_chart':
        return (
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={series}
                dataKey={yKey}
                nameKey={xKey}
                cx="50%"
                cy="50%"
                outerRadius={100}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                labelLine={false}
              >
                {series.map((_, index) => (
                  <Cell key={index} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        );

      case 'radar_chart': {
        // Radar chart for rider comparison
        const categories = ['gc', 'tt', 'sprint', 'climber', 'one_day'];
        const categoryLabels: Record<string, string> = {
          gc: 'GC',
          tt: 'Crono',
          sprint: 'Sprint',
          climber: 'Scalatore',
          one_day: 'Classiche',
        };

        const radarData = categories.map(cat => {
          const point: Record<string, unknown> = { category: categoryLabels[cat] || cat.toUpperCase() };
          series.forEach(rider => {
            const riderName = rider.name as string;
            point[riderName] = (rider[cat] as number) || 0;
          });
          return point;
        });

        return (
          <ResponsiveContainer width="100%" height={350}>
            <RadarChart data={radarData}>
              <PolarGrid stroke="#E5E7EB" />
              <PolarAngleAxis dataKey="category" tick={{ fontSize: 12 }} />
              <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fontSize: 10 }} />
              {series.map((rider, index) => (
                <Radar
                  key={rider.name as string}
                  name={rider.name as string}
                  dataKey={rider.name as string}
                  stroke={COLORS[index % COLORS.length]}
                  fill={COLORS[index % COLORS.length]}
                  fillOpacity={0.3}
                />
              ))}
              <Legend />
              <Tooltip />
            </RadarChart>
          </ResponsiveContainer>
        );
      }

      case 'table':
        return (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  {Object.keys(series[0] || {}).slice(0, 5).map((key) => (
                    <th
                      key={key}
                      className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      {key.replace(/_/g, ' ')}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {series.slice(0, 10).map((row, i) => (
                  <tr key={i} className="hover:bg-gray-50">
                    {Object.values(row).slice(0, 5).map((value, j) => (
                      <td key={j} className="px-4 py-2 text-sm text-gray-900 whitespace-nowrap">
                        {typeof value === 'number' ? value.toLocaleString() : String(value)}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        );

      default:
        return <p className="text-gray-500">Tipo di grafico non supportato</p>;
    }
  };

  return (
    <div className="w-full">
      {title && (
        <h3 className="text-lg font-semibold text-gray-800 mb-4">{title}</h3>
      )}
      {renderChart()}
    </div>
  );
};
