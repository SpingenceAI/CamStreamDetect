import React from "react";
import Card from "@mui/material/Card";

function Card2({ height,prompt,is_ok }) {
  return (
    <div>
      <Card
        style={{
          height: height + "vh",

        }}
      >
        <div
          style={{
            height: height / 8 + "vh",
            backgroundColor: "#124680",
            display: "flex",
            // vertical algin

            alignItems: "center",
          }}
        >
          <div
            style={{
              fontSize: "3rem",
              fontWeight: "bold",
              color: "white",
              marginLeft: "1rem",
            }}
          >
            VLM
          </div>
        </div>
        <div style={{ marginLeft: "1rem" }}>
          <p
            style={{
              fontSize: "5rem",
              fontWeight: "bold",
              color: "gray",
              marginLeft: "1rem",
            }}
          >
            {prompt}
          </p>
        </div>
        <div
          style={{
            marginRight: "3rem",
            display: "flex",
            height:"50%"
          }}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "flex-end",
              alignItems: "flex-end",
              width: "100%",
            }}
          >
            <div
              style={{
                backgroundColor: is_ok?"#5FB83B":"gray",
                width: "15rem",
                height: "5rem",
                borderRadius: "1rem",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
              }}
            >
              <span
                style={{
                  fontSize: "4rem",
                  color: "white",
                  fontWeight: "bold",
                }}
              >
                OK
              </span>
            </div>
            <div
              style={{
                backgroundColor: is_ok?"gray":"#C00000",
                width: "15rem",
                height: "5rem",
                borderRadius: "1rem",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                marginLeft: "3rem",
              }}
            >
              <span
                style={{
                  fontSize: "4rem",
                  color: "white",
                  fontWeight: "bold",
                }}
              >
                NG
              </span>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
}

export default Card2;
