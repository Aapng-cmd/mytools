#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <unordered_map>
#include <random>
#include <algorithm>
#include <cmath>
#include <numeric>

const std::string CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
const size_t CHAR_LEN = CHARACTERS.length();
const int HASH_SIZE = 32;
const long long MODULUS = 60211648199136739;

//long long mod_pow(long long base, long long exp, long long mod) {
//    long long result = 1;
//    base = base % mod;  // Handle the case where base is greater than mod

//    while (exp > 0) {
//        if (exp % 2 == 1) {  // If exp is odd
//            result = (result * base) % mod;
//        }
//        exp = exp >> 1;  // Divide exp by 2
//        base = (base * base) % mod;  // Square the base
//    }
//    return result;
//}

template <typename T>
T mod_pow(T base, T exp, T modulus) {
  base %= modulus;
  T result = 1;
  while (exp > 0) {
    if (exp & 1) result = (result * base) % modulus;
    base = (base * base) % modulus;
    exp >>= 1;
  }
  return result;
}

std::string normal_string(std::string s) {
    size_t s_size = s.size();
    if (s_size == 1) {
        s += static_cast<char>(static_cast<int>(s[0]) ^ HASH_SIZE);
    }
    if (s_size < HASH_SIZE) {
        for (size_t i = s_size; i < HASH_SIZE; ++i) {
            s += CHARACTERS[(static_cast<int>(s[i - s_size]) + static_cast<int>(s[i - s_size + 1])) % CHAR_LEN];
        }
    }
    return s;
}

std::vector<std::string> create_segm_arr(const std::string& s) {
    size_t seg_len = s.size() / HASH_SIZE;
    size_t num_not_norm_seg = s.size() % HASH_SIZE;

    std::vector<std::string> segm;
    for (size_t i = 0; i < s.size() - (num_not_norm_seg * (seg_len + 1)); i += seg_len) {
        segm.push_back(s.substr(i, seg_len));
    }

    for (size_t i = s.size() - (num_not_norm_seg * (seg_len + 1)); i < s.size(); i += seg_len + 1) {
        segm.push_back(s.substr(i, seg_len + 1));
    }

    return segm;
}

long long sum_of_string(const std::string& s) {
    long long sum = 0;
    for (char c : s) {
        sum += static_cast<int>(c);
    }
    return sum;
}

long long cycle_string(const std::string& s) {
    long long start = static_cast<int>(s[0]);
    for (size_t i = 1; i < s.size(); ++i) {
        int ord_val = static_cast<int>(s[i]);
        switch (i % 5) {
            case 0: start += ord_val; break;
            case 1: start /= ord_val; break;
            case 2: start -= ord_val; break;
            case 3: start *= ord_val; break;
            case 4: start = -mod_pow<long long>(start, ord_val, MODULUS); break;  // Use mod_pow here
        }
    }
    return start;
}

std::string hashing(std::vector<std::string> arr) {
    arr.push_back(arr[0]);
    std::vector<char> HASH;
    
    long long prev_cycle = cycle_string(arr[0]);
    for (size_t i = 1; i < arr.size(); ++i) {
        long long current_cycle = cycle_string(arr[i]);
        long long index;
        if (current_cycle < prev_cycle) {
            std::string concatenated_string;
            for (size_t j = i; j < arr.size(); ++j) {
                concatenated_string += arr[j];
            }
            index = mod_pow<long long>(sum_of_string(concatenated_string), std::abs(sum_of_string(arr[i - 1]) << sum_of_string(arr[i])), CHAR_LEN);
        } else {
            std::string concatenated_string;
            for (size_t j = 0; j < i + 1; ++j) {
                concatenated_string += arr[j];
            }
            index = mod_pow<long long>(sum_of_string(concatenated_string), std::abs(sum_of_string(arr[i - 1]) << sum_of_string(arr[i])), CHAR_LEN);
        }
        HASH.push_back(CHARACTERS[index % CHAR_LEN]);
        prev_cycle = current_cycle;
    }
    return std::string(HASH.begin(), HASH.end());
}

std::string hash_string(const std::string& s) {
    return hashing(create_segm_arr(normal_string(s)));
}

std::string generate_random_string(size_t length) {
    std::string result;
    std::random_device rd;
    std::mt19937 generator(rd());
    std::uniform_int_distribution<> distribution(0, CHAR_LEN - 1);
    for (size_t i = 0; i < length; ++i) {
        result += CHARACTERS[distribution(generator)];
    }
    return result;
}

//std::string generate_hash_from_random_string(size_t length) {
//    std::string random_string = generate_random_string(length);
//    return hash_string(random_string);
//}

std::string generate_specific_string(int iteration) {
    if (iteration == 0) {
        return std::string(1, CHARACTERS[0]); // Handle the case for 0
    }

    std::vector<char> result; // Use a vector to store characters
    while (iteration > 0) {
        int remainder = iteration % CHAR_LEN;
        result.push_back(CHARACTERS[remainder]); // Get the character for the remainder
        iteration /= CHAR_LEN; // Integer division
    }

    std::reverse(result.begin(), result.end()); // Reverse the result to get the correct order
    return std::string(result.begin(), result.end()); // Convert vector to string
}

int test() {
    std::unordered_map<std::string, int> HASHMAP; // Equivalent to the Python dictionary
    int stress = (int)pow(10, 8);
    try {
//        std::ofstream f("statistics.txt"); // Open the file for writing
//        if (!f.is_open()) {
//            std::cerr << "Error opening file!" << std::endl;
//            return 1;
//        }

        int k = 0;
        
        for (int i = 0; i < stress; ++i) { // Loop for 1 iteration
            std::string s = generate_specific_string(k); // Generate the specific string
            k += 1;
            std::string h = hash_string(s); // Hash the string
            std::vector<std::string> segments = create_segm_arr(normal_string(s)); // Create segments

//            // Print segments to console (similar to Python's print)
//            for (const auto& segment : segments) {
//                std::cout << segment << " ";
//            }
//            std::cout << std::endl;

            // Write the string and its hash to the file
            // f << s << " " << h << "\n";

            // Update the HASHMAP
            if (HASHMAP.find(h) != HASHMAP.end()) {
                HASHMAP[h] += 1; // Increment count if hash already exists
            } else {
                HASHMAP[h] = 1; // Initialize count to 1
            }
        }
        // f.close(); // Close the file
    } catch (const std::exception& e) {
        std::cerr << "Exception: " << e.what() << std::endl;
    }

    // Collect popular hashes
    std::vector<std::string> popular_hashes;
    for (const auto& pair : HASHMAP) {
        if (pair.second > 1) {
            popular_hashes.push_back(pair.first); // Add to popular hashes if count > 0
        }
    }
    
    int pop_size = popular_hashes.size();
    std::cout << pop_size << "/" << stress << " = " << static_cast<double>(pop_size) / stress << " | With HASH_SIZE = " << HASH_SIZE << std::endl;
    // Print popular hashes
//    for (const auto& hash : popular_hashes) {
//        std::cout << hash << " ";
//    }
    std::cout << std::endl;

    return 0;
}

int main() {
//    std::string input = "a";
//    std::string hashed_output = hash_string(input);
//    std::cout << "Hashed output: " << hashed_output << std::endl;
////    size_t random_length = 10;
////    std::string random_hashed_output = generate_hash_from_random_string(random_length);
////    std::cout << "Random hashed output: " << random_hashed_output << std::endl;
    test();

    return 0;
}
