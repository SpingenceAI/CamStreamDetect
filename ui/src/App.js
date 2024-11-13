
import Header from "./components/Header";
import Body from "./components/Body";
function App() {
  const headerHeight = 10;
  return (
    <div>
      <Header 
        headerHeight={headerHeight}
      />
      <Body 
        headerHeight={headerHeight}
      />
    </div>
  );
}

export default App;
