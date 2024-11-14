import * as React from "react";
import SpingenceLogo from "../assets/SP_LOGO2.png";
function Header({headerHeight}) {

  return (
    <div
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        width: "100%",
        height: headerHeight + "vh",
        backgroundColor: "#F2F2F2",
      }}
    >
      <div
        style={{
          marginLeft: 30,
          marginTop: "1vh",
        }}
      >
        <div>
          <img
            src={SpingenceLogo}
            alt="spingence logo"
            style={{
              width:"40vw",
            }}
          />
        </div>
      </div>
    </div>
  );
}

export default Header;
