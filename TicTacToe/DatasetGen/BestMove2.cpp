#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <utility>

using namespace std;

int win(const vector<int>& board){
    int wins[8][3] = {{0,1,2},{3,4,5},{6,7,8},{0,3,6},
                      {1,4,7},{2,5,8},{0,4,8},{2,4,6}};
    for(int i = 0; i < 8; ++i) {
        if(board[wins[i][0]] != 0 &&
           board[wins[i][0]] == board[wins[i][1]] &&
           board[wins[i][0]] == board[wins[i][2]])
            return board[wins[i][2]];
    }
    return 0;
}

bool over(const vector<int>& board){
    if(win(board)==0) return false;
    else return true;
}

int minimax(vector<int>& board, int player) {
    int winner = win(board);
    if(winner != 0) return winner*player;

    int move = -1;
    int score = -2;
    for(int i = 0; i < 9; ++i) {
        if(board[i] == 0) {
            board[i] = player;
            int thisScore = -minimax(board, player*-1);
            if(thisScore > score) {
                score = thisScore;
                move = i;
            }
            board[i] = 0;
        }
    }
    if(move == -1) return 0;
    return score;
}

int best_move(vector<int> board, bool show=false){
  int move = -1;
  int score = -2;
  for (int i = 0; i < 9; i++) {
    if(board[i] == 0) {
        board[i] = 1;
        int tempScore = -minimax(board, -1);
        board[i] = 0;
        if(tempScore > score) {
            score = tempScore;
            move = i;
        }
    }
  }
  if (show) cout<< move << "\n\n";
  return move;
}

void printBoard(const vector<int>& board){
  for(int i=0;i<3;i++){
    for(int j=0;j<3;j++){
      cout<< board[i*3 + j] << "\t";
    }
    cout<<"\n\n";
  }
}

vector<int> reverseBoard(vector<int> board){
  for(int i=0;i<9;i++){
    board[i]=board[i]*-1;
  }
  return board;
}

void makeMove(vector<int>& board, int playerNum, int move){
  board[move]=playerNum;
}

void demo(vector<int> a,bool againstUser){
  printBoard(a);
  for(int player=-1;!over(a);player=player*-1){
    if (player==1) {
      makeMove(a,1,best_move(a,true));
    }else{
      if(!againstUser){
        makeMove(a,-1,best_move(reverseBoard(a),true));
      }else{
        cout<< "Pick your move (0-8):\n";
        int move;
        cin >> move;
        if(a[move]==0) makeMove(a,-1,move);
      }

    }
    printBoard(a);
  }
}

vector<int> decodeBase3(int coded){
  vector<int> retval;
  for (int i = 0; i < 9; i++) {
    retval.push_back(0);
  }
  for (int i = 8; i >=0; i--) {
    int next = coded/3;
    retval[i]= coded - (next*3) -1;
    coded = next;
  }
  return retval;
}

int main(){
  //Change these booleans for demos
  //demoTime runs demo
  bool demoTime = true;
  //userInput decides whether demos is cpu v cpu or user v cpu
  bool userInput = true;
  vector<int> a;
  //written out for debugging to plug in starting state
  a.push_back(0);
  a.push_back(0);
  a.push_back(0);
  a.push_back(0);
  a.push_back(0);
  a.push_back(0);
  a.push_back(0);
  a.push_back(0);
  a.push_back(0);
  if(demoTime){
    demo(a,userInput);
  }else{
    vector<pair<int,int> > codedBoards;
    string line;
    ifstream boardList ("OutputFiles/nonterminalBoards.txt");
    if (boardList.is_open()){
      while(getline(boardList,line)){
         codedBoards.push_back(pair<int,int>(stoi(line),0));
      }
      boardList.close();
    }

    int num=codedBoards.size();
    cout << "Successfully read " << num << " coded boards\n";

    for (int i = 0; i < num; i++) {
      if (i%100==1) cout << i << "\n";
      codedBoards[i].second = best_move(decodeBase3(codedBoards[i].first));
    }

    ofstream labeledOutput ("OutputFiles/bestMoves.txt");
    if (labeledOutput.is_open()){
      for (int i = 0; i < num; i++) {
        labeledOutput << codedBoards[i].first << ":" << codedBoards[i].second << "\n";
      }
      labeledOutput.close();
    }
  }
  return 0;
}
