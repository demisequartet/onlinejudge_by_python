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
(1, 'HELLO WORLD', 'Hello,World!を出力するプログラムを作成せよ。末尾の改行の有無は問わない',E'Hello,World!\n','NONE', '', '');
INSERT INTO question (question_id, name, question_content,output, difficulty, basename, commentary) VALUES
(2, 'wakayama repeat', '出力例のように、wakayamaを10回表示するプログラムを作成せよ。',E'wakayama\nwakayama\nwakayama\nwakayama\nwakayama\nwakayama\nwakayama\nwakayama\nwakayama\nwakayama\n','NONE', '', '');
INSERT INTO question (question_id, name, question_content,output, difficulty, basename, commentary) VALUES
(3, 'okayama repeat', 'okayamaを10回表示するプログラムを作成せよ。ただし、okayamaと1回表示したあとに改行すること',E'okayama\nokayama\nokayama\nokayama\nokayama\nokayama\nokayama\nokayama\nokayama\nokayama\n','NONE', '', '');
INSERT INTO question (question_id, name, question_content,output, difficulty, basename, commentary) VALUES
(4,'prime number','2から30までの素数を出力せよ。',E'2\n3\n5\n7\n11\n13\n17\n19\n23\n29\n','NONE','','');
INSERT INTO question (question_id, name, question_content,output, difficulty, basename, commentary) VALUES
(5,'HELLO PROGRAMMING','出力例のように、Hello C Programmingと表示するプログラムを作成せよ。なお、printf関数を何回使っても良い。',E'Hello\nC\nProgramming\n','NONE','','');



