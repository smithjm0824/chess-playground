import React from 'react';
import Chessboard from 'chessboardjsx';
import axios from 'axios';
import './App.css';


function timeout(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}


export default class App extends React.Component{
  state = {
    boards : {},
    board : "start"
  }

  async componentDidMount() {
    const response = await axios.get(`http://localhost:5000/`)
    const boards = await response.data;
    
    for (var board in boards){
      if (boards.hasOwnProperty(board)){
        console.log(boards[board]);
        await timeout(500); 
        this.setState(state => ({ board : boards[board] }));
      }
    } 

  }

  render(){
      return (
        <div id="myBoard">
          <Chessboard position={this.state.board}/>
        </div>
      );
  }
}
