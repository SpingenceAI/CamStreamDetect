import React from "react";
import { TextField } from "@mui/material";
import Icon1Src from "../assets/icon1.png";
import Icon2Src from "../assets/icon2.png";
import { setVLMPromptAPI,setVMPromptAPI } from "../apis";
import Backdrop from '@mui/material/Backdrop';
import CircularProgress from '@mui/material/CircularProgress';
function InputBox({ height }) {
  const fontSize = 3;
  const iconSize = "5rem";
  const [loading,isLoading] = React.useState(false);
  const [prompt,setPrompt] = React.useState("");
  const handleUpdateVMPrompt = () =>{
    isLoading(true)
    setVLMPromptAPI(prompt)
    .then((res)=>{
    })
    .catch((err)=>{
        console.log(err)
    }).finally(()=>{
        // wait for 1 second

        const timer = setTimeout(() => {
        isLoading(false)
        setPrompt("")
        }, 1000);
    })
  }
  const handleUpdateVLMPrompt = () =>{
    isLoading(true)
    setVMPromptAPI(prompt)
    .then((res)=>{
    })
    .catch((err)=>{
        console.log(err)
    }).finally(()=>{
        const timer = setTimeout(() => {
            isLoading(false)
            setPrompt("")
            }, 1000);
    })
  }
  return (
    <div>
    <div>
      <Backdrop
        sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
        open={loading}
        onClick={()=>{
            isLoading(false)
        }}
      >
        <CircularProgress color="inherit" />
      </Backdrop>
    </div>
      <div
        style={{
          height: height + "vh",
          width: "100%",
        }}
      >
          <div
            style={{
              display: "flex",
            }}
          >
            <div
              style={{
                fontSize: fontSize + 1 + "rem",
                fontWeight: "bold",
                color: "#124680",
              }}
            >
              條件設定
            </div>
            <div
              style={{
                marginLeft: "auto",
                // vertical algin
                display: "flex",
                alignItems: "center",
              }}
            >
              <img
                style={{
                  hover: "pointer",
                  width: iconSize,
                  height: iconSize,
                }}
                src={Icon1Src}
                alt="icon1"
                onClick={handleUpdateVLMPrompt}
              />
              <img
                style={{
                  hover: "pointer",
                  marginLeft: "3rem",
                  width: iconSize,
                  height: iconSize,
                }}
                onClick={handleUpdateVMPrompt}
                src={Icon2Src}
                alt="icon2"
              />
            </div>
          </div>
          <div>
            <TextField
                value={prompt}
                onChange={(e)=>{
                    setPrompt(e.target.value)
                }}
              inputProps={{
                style: {
                  fontSize: fontSize + "rem",
                  paddingTop: fontSize - 1.5 + "rem",
                  lineHeight: "4rem",
                }
              }} // font size of input text
              fullWidth
              multiline
              rows={3}
              id="fullWidth"
            />
          </div>
      </div>
    </div>
  );
}

export default InputBox;
