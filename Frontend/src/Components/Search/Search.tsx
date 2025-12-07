import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox"
import React, {useState} from "react"
import { Alert, AlertDescription, AlertTitle } from "../ui/alert"
import { AlertCircleIcon } from "lucide-react"
import search from './../../assets/search.svg'

export function Search(){
    const [Search, setSearch] = useState<string>("")
    const [showAlert, setShowAlert] = useState<Boolean>(false)

    const Enter = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()

        try{
            await fetch('http://localhost:5000/news-search', {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({ user_input: Search })
            })
        }catch (error){
            console.error(error)
        }
    }

    return(
        <form onSubmit={Enter}>

            <div className="flex flex-row justify-center">
                
                <div className="bg-sidebar-primary text-ring p-6 m-6 rounded-lg w-4xl
                flex flex-row justify-evenly items-center">
                    
                    <div className="flex flew-row items-center gap-2">
                        <img src={search} alt="Search-icon" className="w-8"/>
                        <button type="submit">Search</button>
                        <input 
                        value={Search}
                        type="text" 
                        placeholder="Enter Company Ticker .JO"
                        className="bg-muted-foreground text-input p-3 rounded-xl pr-18
                        focus: outline-none"
                        required
                        onChange={(e) => setSearch(e.target.value)}
                        />
                    </div>

                    <div className="flex items-center space-x-2">
                        <Checkbox id="terms" />
                        <Label htmlFor="terms">Consider Dividends</Label>
                    </div>

                </div>

                {
                /*
                    Add an ASK AI button which will have a chat bot that tells more 
                    about the company in clear context
                */
                }
                
            </div>

        </form>
    )
}