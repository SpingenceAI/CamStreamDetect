
import React from "react";
import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";

function CardTemplate(){
    return (
        <div>
            <Card>
                <CardContent>
                    <h1>Card 2</h1>
                    <p>Card 2 content</p>
                </CardContent>
                <CardActions>
                    <button>Click me</button>
                </CardActions>
            </Card>
            
        </div>
    )
}

export default CardTemplate;