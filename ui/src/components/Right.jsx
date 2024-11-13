import React from "react";
import Card1 from "./Card1";
import Card2 from "./Card2";
import {
    useEffect,
    useState
} from "react"

import { getStatusAPI } from "../apis";
function Right(){
    const cardHeight = 37.9
    const [status,setStatus] = useState(null)
    useEffect(()=>{
        // every second get the status
        setInterval(()=>{
            getStatusAPI()
            .then((res)=>{
                setStatus(res)
            })
            .catch((err)=>{
                console.log(err)
            })
        },1000)
    },[])
    return (
        <div>
            <div>
                <Card1 
                    height={cardHeight}
                    prompt={status?.vm_prompt}
                    is_ok={status?.vm_is_ok}
                />
            </div>
            <div
                style={{
                    marginTop:30
                }}
            > 
                <Card2 
                    height={cardHeight}
                    prompt={status?.vlm_prompt}
                    is_ok={status?.vlm_is_ok}
                />
            </div>
        </div>
    )
}

export default Right;