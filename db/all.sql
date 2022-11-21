CREATE TABLE question (
    question_id  SERIAL NOT NULL,
    name         text     UNIQUE,
    question_content text     NOT NULL,
    output text NOT NULL,
    difficulty   VARCHAR(10)     DEFAULT 'NONE',
    basename     text     DEFAULT '',
    commentary   text     DEFAULT '',

    PRIMARY KEY (question_id)
);


CREATE TABLE submit (
   response_id  SERIAL NOT NULL,
   student_id   int  NOT NULL,
   question_id  int  NOT NULL,
   result       text NOT NULL,
   source       text NOT NULL,

   PRIMARY KEY (response_id),
   FOREIGN KEY (question_id)
   REFERENCES  question (question_id)

);


INSERT INTO question (question_id, name, question_content,output, difficulty, basename, commentary) VALUES
(1,'HELLO PROGRAMMING','出力例のように、「Hello」 「C」 「Programming」に分けて3行で表示するプログラムを作成してください。なお、printf関数は何回使っても構いません。',E'Hello\nC\nProgramming\n','NONE','','');
-- INSERT INTO question (question_id, name, question_content,output, difficulty, basename, commentary) VALUES
-- (2,'九九','2から30までの素数を出力せよ。',E'2\n3\n5\n7\n11\n13\n17\n19\n23\n29\n','NONE','','');



