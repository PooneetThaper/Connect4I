//FIRST TRY
//NOT WORKING VERSION

#include <iostream>
#include <vector>
using namespace std;

int winAnalysis(vector<int> board,int move);
double contemplateMax(vector<int> board,int move);
double contemplateMin(vector<int> board,int move);

int winAnalysis(vector<int> board,int move){
  int n=move-move%3;
  int count=0;
  int id=board[n];
  for(int i=n;i<n+3;i++){
    if(board[i]==id) count++;
    if(count==3) return id;
  }
  n=move%3;
  count=0;
  id=board[n];
  for(int i=n;i<9;i=i+3){
    if(board[i]==id) count++;
    if(count==3) return id;
  }
  if (move%3==move%6) {
    //0 4 8
    //2 4 6
    n=move;
    id=board[n];
    if(board[4]==id && board[8-n]==id) return id;
  }
  if(move==4){
    id=board[4];
    if(board[0]==id && board[8]==id) return id;
    if(board[2]==id && board[6]==id) return id;
  }
  return 0;
}


double contemplateMax(vector<int> board, int move){
  if(board[move]!=0) return -2;
  board[move]=-1;
  int winstat=winAnalysis(board,move);
  /*
  for (size_t i = 0; i < 9; i++) {
      cout << board[i] << "\t";
  }
  cout <<":"<< winstat << '\n';
  */
  if(winstat!=0) return winstat;

  int best=-1;
  double max=-1;
  double sum=0;
  int count=0;
  for (size_t i = 0; i < 9; i++) {
    if (board[i]==0) {
      count++;
      double k=contemplateMin(board,i);
      sum+=k;
      if(k>=max){
        max=k;
        best=i;
      }
    }
  }
  if(count!=0){
    for(int i=0;i<9;i++){
      //cout<<board[i]<<",\t";
    }
    //cout<<best<<",max:"<<max<<"\n";
    return sum/count;
  }else return 0;
}

double contemplateMin(vector<int> board,int move){
  if(board[move]!=0) return -2;
  board[move]=1;
  int winstat=winAnalysis(board,move);
  /*
  for (size_t i = 0; i < 9; i++) {
      cout << board[i] << "\t";
  }
  cout <<":"<< winstat << '\n';
  */
  if(winstat!=0) return winstat;

  int best=-1;
  double min=1;
  double sum=0;
  int count=0;
  for (size_t i = 0; i < 9; i++) {
    if (board[i]==0) {
      count++;
      double k=contemplateMax(board,i);
      sum+=k;
      if(k<=min){
        min=k;
        best=i;
      }
    }
  }
  if(count!=0){
    for(int i=0;i<9;i++){
      //cout<<board[i]<<",\t";
    }
    //cout<<best<<",min:"<<min<<"\n";
    return sum/count;
  }else return 0;
}

int best_move(vector<int> a){
  double max=-1;
  int best=-1;
  for (size_t i = 0; i < 9; i++) {
    if(a[i]==0){
      double k=contemplateMin(a,i);
      cout<<i<<":"<<k<<"\n";
      if(k>max){
        max=k;
        best=i;
      }
    }
  }
  return best;
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
  cout<<best_move(a)<<"\n";
}
