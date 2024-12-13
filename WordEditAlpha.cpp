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
    /// @brief �ù�궨λ��ָ��λ�á�
    /// @param x λ�õĺ�����
    /// @param y λ�õ�������
    void gotoxy(short x, short y) {
        COORD coord = {x, y}; 
        SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE),coord);
    }
*/

    /// @brief ���ַ������ո���Ϊ��������ո���ַ�����
    /// @param s Ҫ��ֵ��ַ�����
    /// @return �ַ������飬���к������в����ո���ַ�����
    vector<string> dividestring(string s){
        //��������
        vector<string>tmp;

        //�м�����
        string lin;

        //���ַ�������
        istringstream sin(s);
        //ֱ�����ܶ���Ϊֹ
        while(sin>>lin){
            tmp.push_back(lin);
        }
        return tmp;
    }
};
using namespace tools;

struct IO{
    vector<string>wordEnglish;          //Ӣ��
    vector<vector<string>>wordChinese;  //����
    vector<int>wordProficient;          //������
    int n;                              //���ʸ���
    bool Readed;                        //��ȡ
    int bowl[6];                        //������Ͱ

    /// @brief ���
    inline void clear(){
        wordEnglish.clear();
        wordChinese.clear();
        wordProficient.clear();
        n=0;
        Readed=0;
        memset(bowl,0,sizeof bowl);
    }

    /// @brief ��ȡӢ�ﵥ���ļ���
    inline void read(){
        ifstream in("words.dat");

        //���ʸ���
        in>>n;
#ifdef DEBUG
        cerr<<"debug:Reading the file \"words.dat\".\n";
#endif
        for(int i=0;i<n;++i){
            string tmp,tmp2;

            //��ȡ����
            getline(in,tmp);

            //��������
            getline(in,tmp);
            wordEnglish.push_back(tmp);

            //����Ӣ��
            getline(in,tmp);
            wordChinese.push_back(dividestring(tmp));
            
            //����������
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

    /// @brief �����Ӣ�ﵥ���ļ���
    inline void write(){
        if(Readed){
            //��ʽ
            //n
            //<English>
            //<Chinese1> <Chinese2> <Chinese3> ...
            ofstream out("words.dat");

            //���ʸ���
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

    /// @brief ����Ӣ���Ƿ���ȷ��
    /// @param id �� wordEnglish �ı�š�
    /// @param answer ����Ĵ𰸡�
    /// @return ����Ƿ�ƥ�䡣
    ///
    /// ������Χʱ�ᴥ�� out of range ����
    inline bool checkEnglish(int id,string&answer){
        if(id>=wordEnglish.size()||id<0)  throw "IO::checkEnglish:out of range";
        return answer==wordEnglish[id];
    }

    /// @brief ���������Ƿ���ȷ��ֻҪ������һ����ȷ���ɡ�
    /// @param id �� wordChinese �ı�š�
    /// @param answer ����Ĵ𰸡�
    /// @return ����Ƿ�ƥ�䡣
    ///
    /// ������Χʱ�ᴥ�� out of range ����
    inline bool checkChinese(int id,vector<string> answer){
        if(id>=wordEnglish.size()||id<0)  throw "IO::checkEnglish:out of range";
        for(auto x:wordChinese[id])
            for(auto y:answer)
                if(x==y)
                    return 1;
        return 0;
    }

    /// @brief ��ʾӢ�ġ�
    /// @param id �� WordEnglish �ı�š�
    ///
    /// ������Χʱ�ᴥ�� out of range ����
    inline void showEnglish(int id){
        if(id>=wordEnglish.size()||id<0)  throw "IO::checkEnglish:out of range";
        cout<<wordEnglish[id];
    }

    /// @brief ��ʾ����
    /// @param id �� WordChinese �ı�š�
    ///
    /// ������Χʱ�ᴥ�� out of range ����
    inline void showChinese(int id){
        if(id>=wordEnglish.size()||id<0)  throw "IO::checkEnglish:out of range";
        for(auto x:wordChinese[id])
            cout<<x<<' ';
    }

    /// @brief �����ȡ���ʡ�
    /// @return ����id��
    ///
    /// ������1��       10%
    /// ��������2��     30%
    ///��������3-5��    60%
    inline int randomword(){
        int type=0;

        //���
        while(1){
            type=rd()%100;

            //������
            if(type<10)type=1;
            else if(type<40)type=2;
            else type=3;

            //�������
            if(type==1&&bowl[1])break;
            if(type==2&&bowl[2])break;
            if(type==3&&(bowl[3]+bowl[4]+bowl[5]))break;
        }
        int id=0,i=0;

        //�ȸ������
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

    /// @brief ���в��ԣ��������ʣ���
    /// @return �Ƿ���ȷ���˳�����-1��
    inline int test(){
        system("cls");
        cout<<"���뵥���� 0 ���˳���\n";

        //����id
        int id=randomword();
        bool ret;

        //��ʾ����
        if(rd()%2){
            showChinese(id);
            cout<<"\n����������Ӣ�ġ�\n";

            //����Ӣ��
            string s;
            getline(cin,s);
            if(s=="0")return -1;

            //�ж�
            if(checkEnglish(id,s)){
                cout<<"��ȷ��";

                //������-1
                bowl[wordProficient[id]]--;
                if(wordProficient[id]--==1)wordProficient[id]++;
                bowl[wordProficient[id]]++;

                ret=1;
            }
            else{
                cout<<"����ˣ�Ӧ���� ";
                showEnglish(id);
                cout<<"��";

                //������+2
                bowl[wordProficient[id]]--;
                wordProficient[id]=max(wordProficient[id]+2,5);
                bowl[wordProficient[id]]++;
                ret=0;
            }
            cout<<"\n�������������";
            while(_kbhit())_getch();
            _getch();
        }
        //Ӣ��
        else{
            showEnglish(id);
            cout<<"\n�������������ģ�����������Կո�ָ������� ';'��'��'��',' �ȷָ���ֻҪ������һ��������ȷ���ɣ�\n";

            //��������
            string s;
            getline(cin,s);
            if(s=="0")return -1;

            //����
            if(checkChinese(id,dividestring(s))){
                cout<<"��ȷ��\n�𰸣�";
                showChinese(id);

                //������-1
                bowl[wordProficient[id]]--;
                if(wordProficient[id]--==1)wordProficient[id]++;
                bowl[wordProficient[id]]++;

                ret=1;
            }
            else{
                cout<<"����ˣ�Ӧ���ǣ�\n";
                showChinese(id);

                //������+2
                bowl[wordProficient[id]]--;
                wordProficient[id]=max(wordProficient[id]+2,5);
                bowl[wordProficient[id]]++;

                ret=0;
            }
            cout<<"\n�������������";
            while(_kbhit())_getch();
            _getch();
        }
        return ret;
    }

    /// @brief ��ӵ��ʡ�
    inline void addword(){
        system("cls");
        cout<<"1-�ֶ����\n2-�ļ����\n����-�˳�";

        //����
        while(_kbhit())_getch();
        char ch=_getch();

        system("cls");

        //�ֶ����
        if(ch=='1'){
            cout<<"����һ��������0�˳���\n";
            while(1){
                //����Ӣ��
                string en,ch;
                cout<<"������Ӣ�ġ�\n";
                getline(cin,en);

                //����Ϸ�
                if(en==""||en=="0")break;

                //��������
                cout<<"���������ġ�ÿ�����ļ��һ���ո�\n";
                getline(cin,ch);

                //����Ϸ�
                if(ch==""||en=="0")break;

                //�½�����
                ++n;
                wordEnglish.push_back(en);
                wordChinese.push_back(dividestring(ch));
                wordProficient.push_back(5);
                bowl[5]++;
            }
        }
        else if(ch=='2'){
            cout<<"�ļ���ʽ��\n��һ��һ��������ʾ�������ĵ��ʸ�����\n������ÿ���������У�һ��Ӣ��һ�����ġ�\n��ͬ�����ÿո񣨶��� '��'��',' �ȷ��ţ�������\n�ļ���Ҫ��֤Ϊ GBK(ANSI) ���룬������ܳ������⡣\n";
            cout<<"�����ļ�����";

            //�����ļ�
            string name;
            getline(cin,name);

            //��ȡ�ļ�
            ifstream in(name);
            string s;
            int n;
            in>>n;  //���ʸ���
            this->n+=n;
            getline(in,s);  //�������
            for(int i=1;i<=n;++i){
                //����&�½�����
                getline(in,s);
                wordEnglish.push_back(s);
                getline(in,s);
                wordChinese.push_back(dividestring(s));
                wordProficient.push_back(5);
                bowl[5]++;
            }
            cout<<"��ӳɹ����������������\n";
            while(_kbhit())_getch();
            _getch();
        }
    }

    /// @brief ���к�����
    inline void testall(){
        system("cls");
        cout<<"WordEditAlpha v1.1\n";

        //�ж��Ƿ��е���
        if(n==0){
            cout<<"�㻹û��ӵ���Ŷ��\n����������˳�\n";
            while(_kbhit())_getch();
            _getch();
            return;
        }

        //���е���
        while(1){
            int ret=test();
            if(ret==-1)break;
        }

        //����
        write();
    }

    /// @brief ���ձ��ɾ�����ʡ�
    /// @param id ��š�
    /// @return �Ƿ�ɾ���ɹ���
    inline bool deleteword(int id){
        if(id>=n||id<0)return 0;

        //���������ɾ��
        swap(wordEnglish[id],wordEnglish[n-1]);
        swap(wordChinese[id],wordChinese[n-1]);
        swap(wordProficient[id],wordProficient[n-1]);
        bowl[wordProficient[n-1]]--;
        --n;

        return 1;
    }

    /// @brief ����Ӣ��ɾ�����ʡ�
    /// @param enword Ӣ�ĵ��ʡ�
    /// @return ɾ���Ƿ�ɹ���
    inline bool deleteword(string enword){
        bool ret=0;

        //��ѯ���з����������ʲ�ɾ����
        for(int i=0;i<n;++i)
            if(enword==wordEnglish[i]){
                deleteword(i);
                --n;
                ret=1;
            }
        return ret;
    }

    /// @brief ��ӡ���е��ʡ�
    ///
    /// ��ע�������ӡ�ı�ű���ʵ��Ŷ�1��
    inline void printwords(){
        cout<<"���\tӢ��\t����\n";
        for(int i=0;i<n;++i){
            cout<<i+1<<'\t';
            showEnglish(i);
            cout<<'\t';
            showChinese(i);
            cout<<'\n';
        }
    }

    /// @brief ����Ÿ��ĵ��ʡ�
    /// @param id ���ʱ�š�
    /// @param english ���ĺ��Ӣ�ġ�
    /// @param chinese ���ĺ�����ġ�
    /// @return �����Ƿ�ɹ���
    inline bool changeword(int id,string english,vector<string> chinese){
        if(id<0||id>=n) return 0;
        wordEnglish[id]=english,wordChinese[id]=chinese;
        bowl[wordProficient[id]]--;
        wordProficient[id]=5;
        bowl[5]++;
        return 1;
    }

    /// @brief ��ԭ���ʸ��ĵ��ʡ�
    /// @param en ԭ���ʡ�
    /// @param english ���ĺ�Ӣ�ġ�
    /// @param chinese ���ĺ����ġ�
    /// @return �Ƿ���ĳɹ���
    inline bool changeword(string en,string english,vector<string> chinese){
        bool ret=0;

        //�������з��������ĵ��ʡ�
        for(int i=0;i<n;++i){
            if(wordEnglish[i]==en){
                changeword(i,english,chinese);
                ret=1;
            }
        }
        return ret;
    }

    /// @brief ���ݵ���Ӣ���ҵ��ʡ�
    /// @param en ���ʡ�
    /// @return �õ��ʱ�š��Ҳ�������-1��
    inline int find(string en){
        for(int i=0;i<n;++i)
            if(en==wordEnglish[i])
                return i;
        return -1;
    }

    /// @brief ���Ĵʿ���������
    inline void changemain(){
        system("cls");

        //���û�е���
        if(!n){
            cout<<"��û�е��ʣ���ȥ��һЩ�ɣ�\n���������������";
            while(_kbhit())_getch();
            _getch();
            return;
        }

        //ѭ������
        while(1){

            //���ʿ�
            system("cls");
            cout<<"���ʿ�\n";
            printwords();
            cout<<"\n1-ɾ������\n2-���ĵ���\n3-����\n����-�˳�\n";

            //�������
            while(_kbhit())_getch();
            char ch=_getch();

            //ɾ������
            if(ch=='1'){
                cout<<"\n1-�����ɾ��\n2-��Ӣ��ɾ��\n3-ɾ��ȫ��\n";

                //�������
                while(_kbhit())_getch();
                char ch=_getch();

                //�����ɾ��
                if(ch=='1'){
                    cout<<"\n�������ţ�";

                    //�����ţ�����ı�ű�������Ŷ�1��
                    int a;
                    cin>>a;
                    --a;

                    //ɾ��
                    bool ret=deleteword(a);
                    if(ret)cout<<"ɾ���ɹ���\n";
                    else cout<<"ɾ��ʧ�ܣ��������Ƿ���ڣ�\n";
                }
                //������ɾ��
                else if(ch=='2'){
                    cout<<"\n�����뵥�ʣ�";

                    //���뵥��
                    string s;
                    getline(cin,s);

                    //ɾ������
                    bool ret=deleteword(s);
                    if(ret)cout<<"ɾ���ɹ���\n";
                    else cout<<"ɾ��ʧ�ܣ����鵥���Ƿ���ڣ�\n";
                }
                //ȫ��ɾ��
                else if(ch=='3'){
                    cout<<"\nȷ��Ҫȫ��ɾ����\n������е��ʶ��ᶪʧ��\n�� 1 ȷ��ɾ����\n";
                    while(_kbhit())_getch();
                    char ch=_getch();
                    if(ch=='1'){
                        clear();
                        Readed=1;
                        break;
                    }
                }
            }
            //����
            else if(ch=='2'){
                cout<<"\n1-����Ÿ���\n2-��Ӣ�ĸ���\n";

                //�������
                while(_kbhit())_getch();
                char ch=_getch();

                //�����
                if(ch=='1'){
                    cout<<"\n�������ţ�";

                    //������
                    int a;
                    cin>>a;
                    --a;

                    //������Ƿ�Խ��
                    if(a<0||a>=n){
                        cout<<"��Ų����ڣ����������ţ�\n";
                    }
                    else{
                        string en,ch;

                        //�������
                        getline(cin,en);

                        //����Ӣ������
                        cout<<"��������ĺ��Ӣ�ġ�\n";
                        getline(cin,en);
                        cout<<"��������ĺ�����ģ��Կո�ֿ�����\n";
                        getline(cin,ch);

                        //�����ַ���
                        if(en==""||ch==""){
                            cout<<"��⵽���Ϸ��ַ���������ʧ�ܣ�\n";
                        }
                        else{
                            //�޸�
                            bool ret=changeword(a,en,dividestring(ch));
                            if(ret)cout<<"���ĳɹ���\n";
                            else cout<<"����ʧ�ܣ��������Ƿ���ڣ�\n";
                        }
                    }
                }
                //�������޸�
                else if(ch=='2'){
                    cout<<"\n�����뵥�ʣ�";

                    //���뵥��
                    string s;
                    getline(cin,s);

                    //�жϵ����Ƿ����
                    int a=find(s);
                    if(a==-1){
                        cout<<"���ʲ����ڣ��������뵥�ʣ�\n";
                    }
                    else{
                        string en,ch;
                        
                        //������ĺ���
                        cout<<"��������ĺ��Ӣ�ġ�\n";
                        getline(cin,en);
                        cout<<"��������ĺ�����ġ�\n";
                        getline(cin,ch);

                        //�жϺϷ���
                        if(en==""||ch==""){
                            cout<<"��⵽���Ϸ��ַ���������ʧ�ܣ�\n";
                        }
                        else{
                            //����
                            bool ret=changeword(a,en,dividestring(ch));
                            if(ret)cout<<"���ĳɹ���\n";
                            else cout<<"����ʧ�ܣ��������Ƿ���ڣ�\n";
                        }
                    }
                }
            }
            //����
            else if(ch=='3'){
                string s;

                //���뵥��
                cout<<"\n������Ҫ���ҵ�Ӣ�ĵ���\n";
                getline(cin,s);

                //��ѯ�Ƿ����
                int ret=find(s);
                if(ret==-1)cout<<"�õ��ʲ����ڣ�\n";
                else{

                    //Ѱ���������ֵ���
                    cout<<"�ҵ����ʣ�\n���\tӢ��\t����\n";
                    for(int i=0;i<n;++i){
                        if(wordEnglish[i]==s){
                            //���
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
            cout<<"���������������\n";
            while(_kbhit())_getch();
            _getch();
        }
        write();
    }

    /// @brief ���캯����
    IO(){
        clear();
        //read();
    }
    ~IO(){
        write();
    }
};

struct Main{
    /// @brief չʾ�����档
    inline void showmain(){
        system("cls");
        cout<<"WordEditAlpha v1.1\n";
        cout<<"\n1-��ʼ����\n";
        cout<<"2-�ӵ���\n";
        cout<<"3-���ʿ�\n";
        cout<<"\n0-�˳�";
    }

    /// @brief ��������
    inline void main(){
#ifdef DEBUG
        cerr<<"debug:go into the main\n";
#endif
        cout<<"WordEditAlpha v1.1\n";
        cout<<"���ڼ��ص��ʡ���\n";
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