import React from "react";
import { Card } from "@mui/material";
import {streamURL} from "../apis";
function Stream({
    height
}){
    return (
        <div
            
        >
            <Card
                style={{
                    height:height+"vh",
                    backgroundColor: "black",
                }}
            
            >
                <img src={streamURL} alt="stream" style={{width:"100%",height:"100%"}}/>
            </Card>
            
        </div>
    )
}

export default Stream;