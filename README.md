# Huffman


1. Name the steps of JPEG encoding and what kinds of math are used in each:

First it does the discrete cosine transform which requires a lot of linear algebra oh my. Then it goes to Quantization which also uses linear algebra. Then it does entropy coding and finally converts that into a string of bits.

2. How does Huffman Coding play a role in creating the final JPEG bit stream?

After the encoding/reording, it uses huffman encoding to get the final vectors into bits for a string of bits.
