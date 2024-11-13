import React from "react";
import Grid2 from "@mui/material/Unstable_Grid2/Grid2";
import Right from "./Right";
import Left from "./Left";
function Body({ headerHeight }) {
  const middleWidth = 0.1;
  const width = 0.1;
//   const cal = () => {
//     return (12 - 2 * width - middleWidth) / 2;
//   };
  const topMargin = 5;
  

  return (
    <div
      style={{
        position: "absolute",
        top: headerHeight + topMargin + "vh",
        width: "100vw",
      }}
    >
      <div
        style={{
        //   paddingLeft: 30,
        //   paddingRight: 30,
        }}
      >
        <Grid2 container spacing={2}>
          <Grid2 item xs={0.2}></Grid2>
          <Grid2 item xs={6.35}>
            <Left />
          </Grid2>
          <Grid2 item xs={0.1}></Grid2>
          <Grid2 item xs={5.08}>
            <Right />
          </Grid2>
          <Grid2 item xs={0.2}></Grid2>
        </Grid2>
      </div>
    </div>
  );
}

export default Body;
