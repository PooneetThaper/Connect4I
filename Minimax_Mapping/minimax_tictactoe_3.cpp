#include <iostream>
#include <utility>
#include <vector>
using namespace std;

pair<bool,int> score(vector<int> board,int depth);
pair<int,int> Minimax(vector<int> board,int playerNum,int depth);

pair<bool,int> score(vector<int> board,int depth){
  //Return value returns bool for whether or not this is an end state and a score
  //Diagonal win check
  if ((board[0]==board[8] && board[0]==board[4]) || (board[2]==board[6] && board[2]==board[4])){
    if (board[4]==1) return pair<bool,int>(true,10-depth);
    if (board[4]==-1) return pair<bool,int>(true,depth-10);
  }
  //Horizontal win check
  for(int n=0;n<9;n=n+3){
    if (board[n]==board[n+1] && board[n+1]==board[n+2]){
      if (board[n]==1) return pair<bool,int>(true,10-depth);
      if (board[n]==-1) return pair<bool,int>(true,depth-10);
    }
  }
  //Vertical win check
  for(int n=0;n<3;n=n+1){
    if (board[n]==board[n+3] && board[n+3]==board[n+6]){
      if (board[n]==1) return pair<bool,int>(true,10-depth);
      if (board[n]==-1) return pair<bool,int>(true,depth-10);
    }
  }
  //No win found (can either be a draw or a nonterminal state)
  for(int i=0;i<9;i++){
    if (board[i]==0) return pair<bool,int>(false,0);
    //Game still playable
  }
  //Draw (all other cases exhausted)
  return pair<bool,int>(true,0);
}

vector<int> makeMove(vector<int> board,int playerNum,int move){
  board[move]=playerNum;
  return board;
}

pair<int,int> Minimax(vector<int> board,int playerNum,int depth){
  pair<bool,int> currentScore=score(board,depth);
  if(currentScore.first!=0){
    for(int i=0;i<9;i++){
      cout<<board[i]<<"\t";
    }
    cout<< "Player: " <<playerNum<<"\tDepth: "<< depth << "\t" << currentScore.second <<"\n";

    return pair<int,int>(-1,currentScore.second);
  }else{
    int count=0;
    int currentBest;
    int currentBestIndex=-1;
    if(playerNum==1){
      currentBest=-11;
      for(int i=0;i<9;i++){
        if(board[i]==0){
          vector<int> newBoard = makeMove(board,playerNum,i);
          pair<int,int> next = Minimax(newBoard,-1,depth+1);
          /*
          for(int i=0;i<9;i++){
            cout<<board[i]<<"\t";
          }
          cout<< "Player: " <<playerNum<<"\tDepth: "<< depth << "\tMove: " << i << "\t\t" << next.first << "\t" << next.second <<"\n";
          */
          if(next.second > currentBest){
            currentBest = next.second;
            currentBestIndex = i;
          }
        }
      }
    }else{
      currentBest=11;
      for(int i=0;i<9;i++){
        if(board[i]==0){
          vector<int> newBoard = makeMove(board,playerNum,i);
          pair<int,int> next = Minimax(newBoard,1,depth+1);
          /*
          for(int i=0;i<9;i++){
            cout<<board[i]<<"\t";
          }
          cout<< "Player: " <<playerNum<<"\tDepth: "<< depth << "\tMove: " << i << "\t\t" << next.first << "\t" << next.second <<"\n";
          */

          if(next.second < currentBest){
            currentBest = next.second;
            currentBestIndex = i;
          }
        }
      }
    }
    return pair<int,int>(currentBestIndex,currentBest);
  }
}

int main(){
  vector<int> a;
  a.push_back(0);
  a.push_back(0);
  a.push_back(0);
  a.push_back(0);
  a.push_back(0);
  a.push_back(0);
  a.push_back(0);
  a.push_back(0);
  a.push_back(0);
  pair<int,int> result= Minimax(a,1,0);
  cout<<"("<<result.first<<","<<result.second<<")\n";
}
