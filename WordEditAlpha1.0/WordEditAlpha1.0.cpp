#include<iostream>
#include<windows.h>
#include<vector>
#include<fstream>
#include<sstream>
#include<random>
#include<time.h>
#include<conio.h>
using namespace std;

#define wordeditversion "alpha1.0"
//#define DEBUG

mt19937 rd(time(0));

namespace tools{
    /// @brief 让光标定位到指定位置。
    /// @param x 位置的横坐标
    /// @param y 位置的纵坐标
    void gotoxy(short x, short y) {
        COORD coord = {x, y}; 
        SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE),coord);
    }

    /// @brief 把字符串按空格拆分为多个不含空格的字符串。
    /// @param s 要拆分的字符串。
    /// @return 字符串数组，其中含有所有不含空格的字符串。
    vector<string> dividestring(string s){
        vector<string>tmp;
        string lin;
        istringstream sin(s);
        while(sin>>lin){
            tmp.push_back(lin);
        }
        return tmp;
    }
};
using namespace tools;

struct IO{
    vector<string>wordEnglish;
    vector<vector<string>>wordChinese;
    vector<int>wordProficient;
    int n;
    bool Readed;
    int bowl[6];

    /// @brief 读取英语单词文件。
    inline void read(){
        ifstream in("words.dat");
        in>>n;
#ifdef DEBUG
        cerr<<"debug:Reading the file \"words.dat\".\n";
#endif
        for(int i=0;i<n;++i){
            string tmp,tmp2;

            //读取空行
            getline(in,tmp);

            //读入中文
            getline(in,tmp);
            wordEnglish.push_back(tmp);

            //读入英文
            getline(in,tmp);
            wordChinese.push_back(dividestring(tmp));
            
            //读入熟练度
            int a;
            in>>a;
            wordProficient.push_back(a);
            bowl[a]++;
        }
#ifdef DEBUG
    cerr<<"debug:Reading done!\n";
#endif
        Readed=1;
    }

    /// @brief 输出到英语单词文件。
    inline void write(){
        if(Readed){
            //格式
            //n
            //<English>
            //<Chinese1> <Chinese2> <Chinese3> ...
            ofstream out("words.dat");
            out<<n<<'\n';
            for(int i=0;i<n;++i){
                out<<wordEnglish[i]<<'\n';
                for(auto x:wordChinese[i])out<<x<<' ';
                out<<'\n';
                out<<wordProficient[i]<<'\n';
            }
            out.close();
        }
#ifdef DEBUG
        else{
            cerr<<"debug:didn't readed.\n";
        }
#endif
    }

    /// @brief 检验英文是否正确。
    /// @param id 在 wordEnglish 的编号。
    /// @param answer 检验的答案。
    /// @return 与答案是否匹配。
    ///
    /// 超出范围时会触发 out of range 报错。
    inline bool checkEnglish(int id,string&answer){
        if(id>=wordEnglish.size()||id<0)  throw "IO::checkEnglish:out of range";
        return answer==wordEnglish[id];
    }

    /// @brief 检验中文是否正确。只要有其中一个正确即可。
    /// @param id 在 wordChinese 的编号。
    /// @param answer 检验的答案。
    /// @return 与答案是否匹配。
    ///
    /// 超出范围时会触发 out of range 报错。
    inline bool checkChinese(int id,vector<string> answer){
        if(id>=wordEnglish.size()||id<0)  throw "IO::checkEnglish:out of range";
        for(auto x:wordChinese[id])
            for(auto y:answer)
                if(x==y)
                    return 1;
        return 0;
    }

    /// @brief 显示英文。
    /// @param id 在 WordEnglish 的编号。
    ///
    /// 超出范围时会触发 out of range 报错。
    inline void showEnglish(int id){
        if(id>=wordEnglish.size()||id<0)  throw "IO::checkEnglish:out of range";
        cout<<wordEnglish[id];
    }

    /// @brief 显示中文
    /// @param id 在 WordChinese 的编号。
    ///
    /// 超出范围时会触发 out of range 报错。
    inline void showChinese(int id){
        if(id>=wordEnglish.size()||id<0)  throw "IO::checkEnglish:out of range";
        for(auto x:wordChinese[id])
            cout<<x<<' ';
    }

    /// @brief 随机抽取单词。
    /// @return 单词id。
    inline int randomword(){
        int type=0;
        while(1){
            type=rd()%100;
            if(type<10)type=1;
            else if(type<40)type=2;
            else type=3;
            if(type==1&&bowl[1])break;
            if(type==2&&bowl[2])break;
            if(type==3&&(bowl[3]+bowl[4]+bowl[5]))break;
        }
        int id=0,i=0;
        if(type==1){
            type=rd()%bowl[1]+1;
            for(;id<n;++id){
                if(wordProficient[id]==1)++i;
                if(i==type)break;
            }
        }
        else if(type==2){
            type=rd()%bowl[2]+1;
            for(;id<n;++id){
                if(wordProficient[id]==2)++i;
                if(i==type)break;
            }
        }
        else{
            type=rd()%(bowl[3]+bowl[4]+bowl[5])+1;
            for(;id<n;++id){
                if(wordProficient[id]==3||wordProficient[id]==4||wordProficient[id]==5)++i;
                if(i==type)break;
            }
        }
        return id;
    }

    /// @brief 进行测试（单个单词）。
    /// @return 是否正确。退出返回-1。
    inline int test(){
        cout<<"输入单独的 0 以退出。\n";
        int id=randomword();
        bool ret;
        if(rd()%2){
            system("cls");
            showChinese(id);
            cout<<"\n请输入它的英文。\n";
            string s;
            getline(cin,s);
            if(s=="0")return -1;
            if(checkEnglish(id,s)){
                cout<<"正确！";
                bowl[wordProficient[id]]--;
                if(wordProficient[id]--==1)wordProficient[id]++;
                bowl[wordProficient[id]]++;
                ret=1;
            }
            else{
                cout<<"答错了，应该是 ";
                showEnglish(id);
                cout<<"。";
                bowl[wordProficient[id]]--;
                wordProficient[id]=max(wordProficient[id]+2,5);
                bowl[wordProficient[id]]++;
                ret=0;
            }
            cout<<"\n按任意键继续。";
            while(_kbhit())_getch();
            _getch();
        }
        else{
            system("cls");
            showEnglish(id);
            cout<<"\n请输入它的中文（多个中文请以空格分隔而不是 ';'、'；'、',' 等分隔；只要有其中一个中文正确即可）\n";
            string s;
            getline(cin,s);
            if(s=="0")return -1;
            if(checkChinese(id,dividestring(s))){
                cout<<"正确！\n答案：";
                showChinese(id);
                bowl[wordProficient[id]]--;
                if(wordProficient[id]--==1)wordProficient[id]++;
                bowl[wordProficient[id]]++;
                ret=1;
            }
            else{
                cout<<"答错了，应该是：\n";
                showChinese(id);
                bowl[wordProficient[id]]--;
                wordProficient[id]=max(wordProficient[id]+2,5);
                bowl[wordProficient[id]]++;
                ret=0;
            }
            cout<<"\n按任意键继续。";
            while(_kbhit())_getch();
            _getch();
        }
        return ret;
    }

    /// @brief 添加单词。
    inline void addword(){
        system("cls");
        cout<<"1-手动添加\n2-文件添加\n其它-退出";
        while(_kbhit())_getch();
        char ch=_getch();
        system("cls");
        if(ch=='1'){
            cout<<"输入一个单独的0退出。\n";
            while(1){
                string en,ch;
                cout<<"请输入英文。\n";
                getline(cin,en);
                if(en==""||en=="0")break;
                cout<<"请输入中文。每个中文间隔一个空格。\n";
                getline(cin,ch);
                if(ch==""||en=="0")break;
                ++n;
                wordEnglish.push_back(en);
                wordChinese.push_back(dividestring(ch));
                wordProficient.push_back(5);
                bowl[5]++;
            }
        }
        else if(ch=='2'){
            cout<<"文件格式-第一行一个整数表示接下来的单词个数。\n接下来每个单词两行，一行英文一行中文。\n不同中文用空格（而非 '；'、',' 等符号）隔开。\n文件需要保证为 GBK(ANSI) 编码，否则可能出现问题。\n";
            cout<<"输入文件名：";
            string name;
            getline(cin,name);
            ifstream in(name);
            string s;
            int n;
            in>>n;
            this->n+=n;
            getline(cin,s);
            wordEnglish.push_back(s);
            wordChinese.push_back(dividestring(s));
            wordProficient.push_back(5);
            bowl[5]++;
        }
    }

    /// @brief 背诵函数。
    inline void testall(){
        system("cls");

        cout<<"WordEditAlpha v1.0\n";
        if(n==0){
            cout<<"你还没添加单词哦！\n按下任意键退出\n";
            while(_kbhit())_getch();
            _getch();
            return;
        }
        cout<<"背诵单词\n";
        cout<<"输入-1可以退出";
        while(1){
            int ret=test();
            if(ret==-1)break;
        }
        write();
    }

    /// @brief 构造函数。
    IO(){
        wordEnglish.clear();
        wordChinese.clear();
        wordProficient.clear();
        n=0;
        Readed=0;
        memset(bowl,0,sizeof bowl);
        //read();
    }
    ~IO(){
        write();
    }
};

struct Main{
    /// @brief 展示主界面。
    inline void showmain(){
        system("cls");
        cout<<"WordEditAlpha v1.0\n";
        cout<<"\n1-开始背诵\n";
        cout<<"2-加单词\n";
        cout<<"\n0-退出";
    }

    /// @brief 主函数。
    inline void main(){
#ifdef DEBUG
        cerr<<"debug:go into the main\n";
#endif
        cout<<"WordEditAlpha v1.0\n";
        cout<<"正在加载单词……\n";
        IO a;
        a.read();
        showmain();
        while(1){
            while(_kbhit())_getch();
            char ch=_getch();
            if(ch=='1'){
                a.testall();
                showmain();
            }
            else if(ch=='2'){
                a.addword();
                showmain();
            }
            else if(ch=='0'){
                break;
            }
        }
    }
}M;

int main(){
    M.main();
    return 0;
}