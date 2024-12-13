#include<iostream>
#include<windows.h>
#include<vector>
#include<fstream>
#include<sstream>
#include<random>
#include<time.h>
#include<conio.h>
using namespace std;

#define wordeditversion "alpha1.1"
//#define DEBUG

mt19937 rd(time(0));

namespace tools{
/*
    /// @brief 让光标定位到指定位置。
    /// @param x 位置的横坐标
    /// @param y 位置的纵坐标
    void gotoxy(short x, short y) {
        COORD coord = {x, y}; 
        SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE),coord);
    }
*/

    /// @brief 把字符串按空格拆分为多个不含空格的字符串。
    /// @param s 要拆分的字符串。
    /// @return 字符串数组，其中含有所有不含空格的字符串。
    vector<string> dividestring(string s){
        //返回数组
        vector<string>tmp;

        //中间数组
        string lin;

        //从字符串读入
        istringstream sin(s);
        //直到不能读入为止
        while(sin>>lin){
            tmp.push_back(lin);
        }
        return tmp;
    }
};
using namespace tools;

struct IO{
    vector<string>wordEnglish;          //英文
    vector<vector<string>>wordChinese;  //中文
    vector<int>wordProficient;          //熟练度
    int n;                              //单词个数
    bool Readed;                        //读取
    int bowl[6];                        //熟练度桶

    /// @brief 清空
    inline void clear(){
        wordEnglish.clear();
        wordChinese.clear();
        wordProficient.clear();
        n=0;
        Readed=0;
        memset(bowl,0,sizeof bowl);
    }

    /// @brief 读取英语单词文件。
    inline void read(){
        ifstream in("words.dat");

        //单词个数
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

            //单词个数
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
    ///
    /// 熟练（1）       10%
    /// 较熟练（2）     30%
    ///不熟练（3-5）    60%
    inline int randomword(){
        int type=0;

        //随机
        while(1){
            type=rd()%100;

            //熟练度
            if(type<10)type=1;
            else if(type<40)type=2;
            else type=3;

            //检验存在
            if(type==1&&bowl[1])break;
            if(type==2&&bowl[2])break;
            if(type==3&&(bowl[3]+bowl[4]+bowl[5]))break;
        }
        int id=0,i=0;

        //等概率随机
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
        system("cls");
        cout<<"输入单独的 0 以退出。\n";

        //单词id
        int id=randomword();
        bool ret;

        //显示中文
        if(rd()%2){
            showChinese(id);
            cout<<"\n请输入它的英文。\n";

            //输入英文
            string s;
            getline(cin,s);
            if(s=="0")return -1;

            //判断
            if(checkEnglish(id,s)){
                cout<<"正确！";

                //熟练度-1
                bowl[wordProficient[id]]--;
                if(wordProficient[id]--==1)wordProficient[id]++;
                bowl[wordProficient[id]]++;

                ret=1;
            }
            else{
                cout<<"答错了，应该是 ";
                showEnglish(id);
                cout<<"。";

                //熟练度+2
                bowl[wordProficient[id]]--;
                wordProficient[id]=max(wordProficient[id]+2,5);
                bowl[wordProficient[id]]++;
                ret=0;
            }
            cout<<"\n按任意键继续。";
            while(_kbhit())_getch();
            _getch();
        }
        //英文
        else{
            showEnglish(id);
            cout<<"\n请输入它的中文（多个中文请以空格分隔而不是 ';'、'；'、',' 等分隔；只要有其中一个中文正确即可）\n";

            //输入中文
            string s;
            getline(cin,s);
            if(s=="0")return -1;

            //检验
            if(checkChinese(id,dividestring(s))){
                cout<<"正确！\n答案：";
                showChinese(id);

                //熟练度-1
                bowl[wordProficient[id]]--;
                if(wordProficient[id]--==1)wordProficient[id]++;
                bowl[wordProficient[id]]++;

                ret=1;
            }
            else{
                cout<<"答错了，应该是：\n";
                showChinese(id);

                //熟练度+2
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

        //读入
        while(_kbhit())_getch();
        char ch=_getch();

        system("cls");

        //手动添加
        if(ch=='1'){
            cout<<"输入一个单独的0退出。\n";
            while(1){
                //输入英文
                string en,ch;
                cout<<"请输入英文。\n";
                getline(cin,en);

                //检验合法
                if(en==""||en=="0")break;

                //输入中文
                cout<<"请输入中文。每个中文间隔一个空格。\n";
                getline(cin,ch);

                //检验合法
                if(ch==""||en=="0")break;

                //新建单词
                ++n;
                wordEnglish.push_back(en);
                wordChinese.push_back(dividestring(ch));
                wordProficient.push_back(5);
                bowl[5]++;
            }
        }
        else if(ch=='2'){
            cout<<"文件格式：\n第一行一个整数表示接下来的单词个数。\n接下来每个单词两行，一行英文一行中文。\n不同中文用空格（而非 '；'、',' 等符号）隔开。\n文件需要保证为 GBK(ANSI) 编码，否则可能出现问题。\n";
            cout<<"输入文件名：";

            //输入文件
            string name;
            getline(cin,name);

            //读取文件
            ifstream in(name);
            string s;
            int n;
            in>>n;  //单词个数
            this->n+=n;
            getline(in,s);  //读入空行
            for(int i=1;i<=n;++i){
                //读入&新建单词
                getline(in,s);
                wordEnglish.push_back(s);
                getline(in,s);
                wordChinese.push_back(dividestring(s));
                wordProficient.push_back(5);
                bowl[5]++;
            }
            cout<<"添加成功！按任意键继续。\n";
            while(_kbhit())_getch();
            _getch();
        }
    }

    /// @brief 背诵函数。
    inline void testall(){
        system("cls");
        cout<<"WordEditAlpha v1.1\n";

        //判断是否有单词
        if(n==0){
            cout<<"你还没添加单词哦！\n按下任意键退出\n";
            while(_kbhit())_getch();
            _getch();
            return;
        }

        //背诵单词
        while(1){
            int ret=test();
            if(ret==-1)break;
        }

        //保存
        write();
    }

    /// @brief 按照编号删除单词。
    /// @param id 编号。
    /// @return 是否删除成功。
    inline bool deleteword(int id){
        if(id>=n||id<0)return 0;

        //换到最后再删除
        swap(wordEnglish[id],wordEnglish[n-1]);
        swap(wordChinese[id],wordChinese[n-1]);
        swap(wordProficient[id],wordProficient[n-1]);
        bowl[wordProficient[n-1]]--;
        --n;

        return 1;
    }

    /// @brief 按照英文删除单词。
    /// @param enword 英文单词。
    /// @return 删除是否成功。
    inline bool deleteword(string enword){
        bool ret=0;

        //查询所有符合条件单词并删除。
        for(int i=0;i<n;++i)
            if(enword==wordEnglish[i]){
                deleteword(i);
                --n;
                ret=1;
            }
        return ret;
    }

    /// @brief 打印所有单词。
    ///
    /// 请注意这里打印的编号比真实编号多1。
    inline void printwords(){
        cout<<"编号\t英文\t中文\n";
        for(int i=0;i<n;++i){
            cout<<i+1<<'\t';
            showEnglish(i);
            cout<<'\t';
            showChinese(i);
            cout<<'\n';
        }
    }

    /// @brief 按编号更改单词。
    /// @param id 单词编号。
    /// @param english 更改后的英文。
    /// @param chinese 更改后的中文。
    /// @return 更改是否成功。
    inline bool changeword(int id,string english,vector<string> chinese){
        if(id<0||id>=n) return 0;
        wordEnglish[id]=english,wordChinese[id]=chinese;
        bowl[wordProficient[id]]--;
        wordProficient[id]=5;
        bowl[5]++;
        return 1;
    }

    /// @brief 按原单词更改单词。
    /// @param en 原单词。
    /// @param english 更改后英文。
    /// @param chinese 更改后中文。
    /// @return 是否更改成功。
    inline bool changeword(string en,string english,vector<string> chinese){
        bool ret=0;

        //更改所有符合条件的单词。
        for(int i=0;i<n;++i){
            if(wordEnglish[i]==en){
                changeword(i,english,chinese);
                ret=1;
            }
        }
        return ret;
    }

    /// @brief 根据单词英文找单词。
    /// @param en 单词。
    /// @return 该单词编号。找不到返回-1。
    inline int find(string en){
        for(int i=0;i<n;++i)
            if(en==wordEnglish[i])
                return i;
        return -1;
    }

    /// @brief 更改词库主函数。
    inline void changemain(){
        system("cls");

        //如果没有单词
        if(!n){
            cout<<"还没有单词，快去加一些吧！\n按下任意键继续。";
            while(_kbhit())_getch();
            _getch();
            return;
        }

        //循环处理
        while(1){

            //单词库
            system("cls");
            cout<<"单词库\n";
            printwords();
            cout<<"\n1-删除单词\n2-更改单词\n3-查找\n其它-退出\n";

            //检测输入
            while(_kbhit())_getch();
            char ch=_getch();

            //删除单词
            if(ch=='1'){
                cout<<"\n1-按编号删除\n2-按英文删除\n3-删除全部\n";

                //检测输入
                while(_kbhit())_getch();
                char ch=_getch();

                //按编号删除
                if(ch=='1'){
                    cout<<"\n请输入编号：";

                    //输入编号（输出的编号比真正编号多1）
                    int a;
                    cin>>a;
                    --a;

                    //删除
                    bool ret=deleteword(a);
                    if(ret)cout<<"删除成功！\n";
                    else cout<<"删除失败，请检查编号是否存在！\n";
                }
                //按单词删除
                else if(ch=='2'){
                    cout<<"\n请输入单词：";

                    //读入单词
                    string s;
                    getline(cin,s);

                    //删除部分
                    bool ret=deleteword(s);
                    if(ret)cout<<"删除成功！\n";
                    else cout<<"删除失败，请检查单词是否存在！\n";
                }
                //全部删除
                else if(ch=='3'){
                    cout<<"\n确定要全部删除吗？\n你的所有单词都会丢失！\n按 1 确定删除。\n";
                    while(_kbhit())_getch();
                    char ch=_getch();
                    if(ch=='1'){
                        clear();
                        Readed=1;
                        break;
                    }
                }
            }
            //更改
            else if(ch=='2'){
                cout<<"\n1-按编号更改\n2-按英文更改\n";

                //检测输入
                while(_kbhit())_getch();
                char ch=_getch();

                //按编号
                if(ch=='1'){
                    cout<<"\n请输入编号：";

                    //输入编号
                    int a;
                    cin>>a;
                    --a;

                    //检测编号是否越界
                    if(a<0||a>=n){
                        cout<<"编号不存在！请检查输入编号！\n";
                    }
                    else{
                        string en,ch;

                        //读入空行
                        getline(cin,en);

                        //读入英文中文
                        cout<<"请输入更改后的英文。\n";
                        getline(cin,en);
                        cout<<"请输入更改后的中文（以空格分开）。\n";
                        getline(cin,ch);

                        //检测空字符串
                        if(en==""||ch==""){
                            cout<<"检测到不合法字符串，更改失败！\n";
                        }
                        else{
                            //修改
                            bool ret=changeword(a,en,dividestring(ch));
                            if(ret)cout<<"更改成功！\n";
                            else cout<<"更改失败，请检查编号是否存在！\n";
                        }
                    }
                }
                //按单词修改
                else if(ch=='2'){
                    cout<<"\n请输入单词：";

                    //读入单词
                    string s;
                    getline(cin,s);

                    //判断单词是否存在
                    int a=find(s);
                    if(a==-1){
                        cout<<"单词不存在！请检查输入单词！\n";
                    }
                    else{
                        string en,ch;
                        
                        //读入更改后结果
                        cout<<"请输入更改后的英文。\n";
                        getline(cin,en);
                        cout<<"请输入更改后的中文。\n";
                        getline(cin,ch);

                        //判断合法性
                        if(en==""||ch==""){
                            cout<<"检测到不合法字符串，更改失败！\n";
                        }
                        else{
                            //更改
                            bool ret=changeword(a,en,dividestring(ch));
                            if(ret)cout<<"更改成功！\n";
                            else cout<<"更改失败，请检查编号是否存在！\n";
                        }
                    }
                }
            }
            //查找
            else if(ch=='3'){
                string s;

                //读入单词
                cout<<"\n请输入要查找的英文单词\n";
                getline(cin,s);

                //查询是否存在
                int ret=find(s);
                if(ret==-1)cout<<"该单词不存在！\n";
                else{

                    //寻找所有这种单词
                    cout<<"找到单词：\n编号\t英文\t中文\n";
                    for(int i=0;i<n;++i){
                        if(wordEnglish[i]==s){
                            //输出
                            cout<<i+1<<'\t';
                            showEnglish(i);
                            cout<<'\t';
                            showChinese(i);
                            cout<<'\n';
                        }
                    }
                }
            }
            else break;
            cout<<"按下任意键继续。\n";
            while(_kbhit())_getch();
            _getch();
        }
        write();
    }

    /// @brief 构造函数。
    IO(){
        clear();
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
        cout<<"WordEditAlpha v1.1\n";
        cout<<"\n1-开始背诵\n";
        cout<<"2-加单词\n";
        cout<<"3-单词库\n";
        cout<<"\n0-退出";
    }

    /// @brief 主函数。
    inline void main(){
#ifdef DEBUG
        cerr<<"debug:go into the main\n";
#endif
        cout<<"WordEditAlpha v1.1\n";
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
            else if(ch=='3'){
                a.changemain();
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