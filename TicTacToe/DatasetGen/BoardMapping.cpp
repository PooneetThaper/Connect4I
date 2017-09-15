// This file aims to traverse the game tree of TicTacToe in order to extract and label all possible gamestates as either terminating or non-terminating states in order to allow other portions of this project to use that data and limit their efforts in finding the best moves only for non-terminating boards.
#include <iostream>
#include <utility>
#include <vector>
#include <algorithm>
#include <fstream>
using namespace std;

vector<int> nonterminalBoards;
vector<int> terminalBoards;

pair<bool,int> score(const vector<int>& board,const int& depth);
vector<int> makeMove(vector<int> board,const int& playerNum,const int& move);
pair<int,int> Minimax(const vector<int>& board,const int& playerNum,const int& depth);
void removeDuplicates(vector<int>& source);
int convertToBase3(const vector<int>& board);
void SortAndSave();

pair<bool,int> score(const vector<int>& board,const int& depth){
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

vector<int> makeMove(vector<int> board,const int& playerNum,const int& move){
  board[move]=playerNum;
  return board;
}

pair<int,int> Minimax(const vector<int>& board,const int& playerNum,const int& depth){
  pair<bool,int> currentScore=score(board,depth);
  if(currentScore.first!=0){
    /*
    for(int i=0;i<9;i++){
      cout<<board[i]<<"\t";
    }
    cout<< "Player: " <<playerNum<<"\tDepth: "<< depth << "\t" << currentScore.second <<"\n";
    */
    terminalBoards.push_back(convertToBase3(board));
    return pair<int,int>(-1,currentScore.second);
  }else{
    nonterminalBoards.push_back(convertToBase3(board));
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

//convert to hashable and easily stored/parsed int using base 3
//board value converted to base 3 ( -1 -> 0 , 0 -> 1 , 1 -> 2 )
//each value converted to int and added to sum
int convertToBase3(const vector<int>& board){
  int sum=0;
  int multiplier = 1;
  for (int i = 8; i >= 0; i--) {
    sum += multiplier * (board[i] + 1);
    multiplier *= 3;
    //cout << sum << "\t" << multiplier << "\n";
  }
  return sum;
}

void removeDuplicates(vector<int>& source){
  int numDeleted = 0;
  for (int i = 0; i < (source.size()-1); i++) {
    //cout << i << "\n";
    if(source[i]==source[i+1]){
      numDeleted++;
      source.erase(source.begin()+i);
      i--;
    }
  }
}

void SortAndSave(){
  sort(nonterminalBoards.begin(),nonterminalBoards.end());
  sort(terminalBoards.begin(),terminalBoards.end());
  removeDuplicates(nonterminalBoards);
  removeDuplicates(terminalBoards);
  cout << "Nonterminal: "<< nonterminalBoards.size() <<"\n";
  cout << "Terminal: "<< terminalBoards.size() <<"\n";

  ofstream a ("OutputFiles/nonterminalBoards.txt");
  if (a.is_open()){
    for (size_t i = 0; i < nonterminalBoards.size(); i++) {
      a << nonterminalBoards[i] << "\n";
    }
    a.close();
  }

  ofstream b ("OutputFiles/terminalBoards.txt");
  if (b.is_open()){
    for (size_t i = 0; i < terminalBoards.size(); i++) {
      b << terminalBoards[i] << "\n";
    }
    b.close();
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
  //cout << convertToBase3(a) << "\n";
  pair<int,int> result= Minimax(a,1,0);
  cout<<"("<<result.first<<","<<result.second<<")\n";
  SortAndSave();

  return 0;
}
