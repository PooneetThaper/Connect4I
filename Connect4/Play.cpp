#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <utility>
#include <memory>
#include <stdexcept>
#include <cstdio>
#include <sstream>
using namespace std;

int svm(const char* cmd) {
    char buffer[128];
    string result = "";
    shared_ptr<FILE> pipe(popen(cmd, "r"), pclose);
    if (!pipe) throw runtime_error("popen() failed!");
    while (!feof(pipe.get())) {
        if (fgets(buffer, 128, pipe.get()) != NULL)
            result += buffer;
    }
    int x=0;
    stringstream convert(result);
    convert>>x;
    return x;
}

char getChar(int i){
  switch(i){
    case 0:
      return '_';
    case 1:
      return 'O';
    case -1:
      return 'X';
  }
  return '?';
}

void printBoard(const vector<int>& board){
  for(int i=0;i < 6;i++){
    for(int j=0;j < 7;j++){
      cout<< getChar(board[i*7 + j]) << "\t";
    }
    cout<<"\n\n";
  }
  cout << "\n";
}

vector<int> reverseBoard(vector<int> board){
  for(int i=0;i<9;i++){
    board[i]=board[i]*-1;
  }
  return board;
}

bool makeMove(vector<int>& board, int playerNum, int move){
  int start = 35+move;
  while(start >= 0){
    if(board[start]==0){
      board[start]=playerNum;
      return true;
    }else{
      start -= 7;
    }
  }
  return false;
}

void removeMove(vector<int>& board, int move){
  int start = 28+move;
  while(start >= 0){
    if(board[start]==0){
      board[start+7]=0;
      return;
    }else{
      start -= 7;
    }
  }
  board[move]=0;
}

int win(const vector<int>& board){
    //int diagWins[2][4][4] = { {{1,0,0,0},{0,1,0,0},{0,0,1,0},{0,0,0,1}},/*Diagonal negative slope*/
    //                          {{0,0,0,1},{0,0,1,0},{0,1,0,0},{1,0,0,0}} /*Diagonal positive slope*/};

    int wins[4][4] = {  {0,8,16,24},/*Diagonal negative slope*/
                        {6,12,18,13},/*Diagonal positive slope*/
                        {0,1,2,3},/*Horizontal*/
                        {0,7,14,21}/*Vertical*/};
    for(int i = 0; i < 6; i++) {
      for (int j = 0; j < 7; j++) {
        if(i < 3){//Vertical or diagonal win possible
          if(j < 4){//Diagonal win possible
            //Check for diagonal win
            int sumNegDiag = 0;
            int sumPosDiag = 0;
            for(int k = 0;k<4;k++){
              sumNegDiag += board[7*i+j+wins[0][k]];
              sumPosDiag += board[7*i+j+wins[1][k]];
            }
            if (sumNegDiag==4 || sumPosDiag==4) return 1;
            if (sumNegDiag==-4 || sumPosDiag==-4) return -1;
          }

          //Check for veritcal win
          int sumVert = 0;
          for(int k = 0;k<4;k++){
            sumVert += board[7*i+j+wins[3][k]];
          }
          if (sumVert==4) return 1;
          if (sumVert==-4) return -1;
        }

        if(j < 4){//Horizontal win possible
          //Check for horizontal win
          int sumHoriz = 0;
          for(int k = 0;k<4;k++){
            sumHoriz += board[7*i+j+wins[2][k]];
          }
          if (sumHoriz==4) return 1;
          if (sumHoriz==-4) return -1;
        }
      }
    }
    return 0;
}

bool over(const vector<int>& board){
    if(win(board)==0) {
      //If not win and top row is empty then not over
      for (int i = 0; i < 7; i++) {
        if (board[i]==0) return false;
      }
    }
    return true;
}

int minimax(vector<int>& board, int player, int depth = 0) {
    int winner = win(board);
    if(winner != 0) {
      cout << depth << ", " << player << " wins here\n";
      return winner*player;
    }
    if(over(board)){
      cout << depth << ",DRAW HERE\n";
      printBoard(board);
    }

    int move = -1;
    int score = -2;
    for(int i = 0; i < 7; i++) {
        if(board[i] == 0) {
            cout << depth << ", " << player<< " is currently exploring: " << i << "\n";
            makeMove(board,player,i);
            int thisScore = -minimax(board, player*-1, depth+1);
            if(thisScore > score) {
                score = thisScore;
                move = i;
            }
            removeMove(board,i);
        }
    }
    if(move == -1) return 0;
    return score;
}

int best_move(vector<int> a, bool mini){
  bool show=true;
  if (mini){
    int move = -1;
    int score = -2;
    for (int i = 0; i < 7; i++) {
      if(a[i] == 0) {
          cout << "Currently exploring from start: " << i << "\n";
          makeMove(a,1,i);
          int tempScore = -minimax(a, -1);
          removeMove(a,i);
          if(tempScore > score) {
              score = tempScore;
              move = i;
          }
      }
    }
    if (show) cout<< move << "\n\n";
    return move;
  }else{
    string input;
    for (int i = 0; i < a.size(); i++) {
      input.append(to_string(a[i]+1));
    }

    string command= "python playSVM.py '"+input+"'";
    cout << command << "\n";
    char cmd[32];
    for (size_t i = 0; i < 32; i++) {
      cmd[i]=command[i];
    }
    return svm(cmd);
  }
}



void demo(vector<int> a,bool againstUser,bool m=true){
  printBoard(a);
  for(int player=-1;!over(a);player*=-1){
    cout << "Current player is: "<<player<<"\n";
    if (player==1) {
      makeMove(a,1,best_move(a,m));
    }else{
      if(!againstUser){
        makeMove(a,-1,best_move(reverseBoard(a),m));
      }else{
        cout<< "Pick your move (0-6):\n";
        int move;
        cin >> move;
        if(a[move]==0) makeMove(a,-1,move);
      }

    }
    printBoard(a);
  }
}

int main(){
  //Change these booleans for demos
  //userInput decides whether demos is cpu v cpu or user v cpu
  bool userInput = true;
  //play against live minimax evaluation or pretrained svm
  bool minimax = true;
  vector<int> a;
  //written out for debugging to plug in starting state
  for (int i = 0; i < 42; i++) {
    a.push_back(0);
  }

  demo(a,userInput,minimax);
  printBoard(a);

  return 0;
}
