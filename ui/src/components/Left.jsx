import React from "react";
import Stream from "./Stream";
import InputBox from "./InputBox";

function Left() {
  const StreamHeight = 60;
  const inputHeight = 16;
  return (
    <div>
      <div>
        <Stream height={StreamHeight} />
      </div>
      {/* <div
        style={{height:"1vh"}}
      ></div> */}
      <div style={{ marginTop: 30 }}>
        <InputBox height={inputHeight} />
      </div>
    </div>
  );
}

export default Left;
