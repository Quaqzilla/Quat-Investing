import { TrendingUp } from "lucide-react"
import { useState } from "react"
import { CartesianGrid, Line, LineChart, XAxis } from "recharts"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"

const chartData = [
  { month: "January", desktop: 186 },
  { month: "February", desktop: 305 },
  { month: "March", desktop: 237 },
  { month: "April", desktop: 73 },
  { month: "May", desktop: 209 },
  { month: "June", desktop: 214 },
  {/*Map the data here from a JSON file that will store all backend output || use the backend mapping*/}
]
const chartConfig = {
  desktop: {
    label: "Desktop",
    color: "var(--chart-4)",
  },
} 

export function Graph(){
  const [signal, setSignal] = useState<string>("")

  const Type = async(e) => {
    e.preventDefault()

    
  }

    return(

        <div className="ml-1 mr-1 p-3 flex md:flex-row justify-evenly sm:flex-col">
            
            <div className="w-full max-w-md p-3 bg-foreground">
                <Card className="w-lg bg-sidebar-primary border-none text-sidebar-ring">
                    <CardHeader>
                        <CardTitle>1 Year Stock Chart data</CardTitle>
                        <CardDescription></CardDescription>
                    </CardHeader>
                    <CardContent>
                        <ChartContainer config={chartConfig}>
                        <LineChart
                            accessibilityLayer
                            data={chartData}
                            margin={{
                            left: 12,
                            right: 12,
                            }}
                            width={500}
                            height={500}
                        >
                            <CartesianGrid vertical={false} />
                            <XAxis
                            dataKey="month"
                            tickLine={false}
                            axisLine={false}
                            tickMargin={8}
                            tickFormatter={(value) => value.slice(0, 3)}
                            />
                            <ChartTooltip
                            cursor={true}
                            content={<ChartTooltipContent hideLabel />}
                            />
                            <Line
                            dataKey="desktop"
                            type="natural"
                            stroke="var(--sidebar-ring)"
                            strokeWidth={2}
                            dot={true}
                            />
                        </LineChart>
                        </ChartContainer>
                    </CardContent>
                </Card>
            </div>

            <div className="w-full max-w-sm m-2.5 p-5 bg-sidebar-primary rounded-2xl
            flex flex-col justify-around">
                
                <div>
                    <h1 className="text-3xl text-sidebar-ring mb-1">Company Valuation</h1>
                    <p className="text-xl font-thin">Valuation:</p>
                </div>

                <div>
                    <h1 className="text-3xl text-sidebar-ring mb-1">Dividends Yield</h1>
                    <p className="text-xl font-thin">Company Threshold: </p>
                    <p className="text-xl font-thin">Minimum JSE Threshold: 6.4%</p>
                </div>

                <div>
                    <h1 className="text-3xl text-sidebar-ring mb-1">Suggestion Signal</h1>
                    <p className="text-xl font-thin">Signal: </p>
                </div>
                
                
            </div>

        </div>
    )
}