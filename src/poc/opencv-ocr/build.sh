rm main
g++ -std=c++14 -o3 -Wall $(pkg-config --cflags --libs tesseract opencv) main.cpp -o main