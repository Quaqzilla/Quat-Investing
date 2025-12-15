import { useState, useEffect } from 'react'
import './App.css'
import { Line, LineChart, XAxis, YAxis, Tooltip, CartesianGrid, ReferenceLine, ResponsiveContainer} from "recharts"
import type { StockApiPayLoad } from "./Data/types"
import type { ChartDataPoint } from "./Data/types"


function App() {
  const [userInput, setUserInput] = useState<string>("");
  const [ticker, setTicker] = useState<string>("");
  const [chartData, setChartData] = useState<ChartDataPoint[]>([]);
  const [intrinsic, setIntrinsic] = useState<string>("");

  useEffect(() => {
    if (!ticker) return;

    const fetchData = async () => {
      try{
        const res = await fetch(`http://127.0.0.1:5000/api/stock/${ticker}`);
        const result: StockApiPayLoad = await res.json();

        const formatted: ChartDataPoint[] = result.data.map((item) => ({
          date: new Date(item.Date).toLocaleDateString("en-US", {
            month: "short",
            day: "numeric"
          }),
          close: item.Close,
          zscore: item["Z-score"],
          anomaly: item.Anomaly
        }));
        {/*Pass the formatted Json data to the empty const*/}
        setChartData(formatted);
        setIntrinsic(result.signal)
      } catch (error) {
        console.error("There has been an error due to: ", error);
      }
    }; 
    fetchData();
  }, [ticker]);

  return (
    <div className='h-full w-full flex flex-col gap-4 bg-black p-2 pb-5 md:p-4'>

        {/*Search bar used to input all the ticker information */}
        <div className='flex flex-row justify-evenly items-center p-3 md:justify-center md:gap-8'>
            <input 
            type="text" 
            placeholder='Please enter your desired stock ticker' 
            required
            className='border bg-white border-solid rounded-3xl py-3 px-4 md:w-100'
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            />
            <button
            type='submit' 
            className='bg-gray-900 py-3 px-4 rounded-lg font-medium text-white'
            onClick={() => setTicker(userInput)}
            >SEARCH</button>
        </div>

        <div className='flex flex-col gap-4 md:flex-row md:justify-evenly'>
            <div className="flex flex-col gap-6 bg-gray-900 p-4 rounded-2xl w-full md:m-2">
              <ResponsiveContainer width="100%" height={200}>
                {/* Close Price Chart */}
                <LineChart width={700} height={250} data={chartData}>
                  <CartesianGrid stroke="#374151"/>
                  <XAxis dataKey="date" />
                  <YAxis label={{ value: 'Stock Price', angle: -90, position: 'insideLeft' }}/>
                  <Tooltip contentStyle={{ backgroundColor: "#1F2937", borderColor: "#4B5563", color: "#F9FAFB" }}/>
                  <Line type="monotone" dataKey="close" stroke="#9CA3AF" strokeWidth={2} dot={false} />
                </LineChart>
              </ResponsiveContainer>
              

             <ResponsiveContainer width="100%" height={150}>
               {/* Z-score Chart */}
                <LineChart width={700} height={150} data={chartData}>
                  <CartesianGrid stroke="#374151" />
                  <XAxis dataKey="date" />
                  <YAxis label={{ value: 'Z-score', angle: -90, position: 'insideLeft' }} />
                  <Tooltip contentStyle={{ backgroundColor: "#1F2937", borderColor: "#4B5563", color: "#F9FAFB" }}/>
                  <Line type="monotone" dataKey="zscore" stroke="#fefefe" strokeWidth={2} dot={false} />
                  <ReferenceLine y={2} stroke="red" strokeDasharray="3 3" label="Upper Threshold" />
                  <ReferenceLine y={-2} stroke="green" strokeDasharray="3 3" label="Lower Threshold" />
                </LineChart>
             </ResponsiveContainer>

            </div>

            <div className='w-full max-w-sm bg-gray-900 h-[150] rounded-2xl text-white p-3 flex flex-col'>
                <h1 className='text-2xl font-light flex justify-center p-2 md:text-4xl'>Intrinsic Value</h1>
                <div className='flex flex-col justify-evenly items-center mt-2'>
                  <h1 className='text-2xl text-gray-400 '>Current Valuation: <b>{intrinsic || "Loading..."}</b> </h1>
                </div>
            </div>
        </div>

        <div className="flex flex-col gap-6 bg-gray-900 p-4 rounded-2xl w-full text-white md:m-2">
            <h1 className='text-2xl font-light flex justify-center p-2 md:text-4xl'>Simplified Financial News</h1>
            <div className='flex flex-col justify-evenly items-center'>
                <h1 className='text-xl text-gray-400 md:text-2xl'>Financial News Coming Soon</h1>
            </div>
        </div>

    </div>
  )
}

export default App
