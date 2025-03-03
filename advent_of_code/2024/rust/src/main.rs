use std::{fs, str::Lines};

fn main() {
    let path = "../../input/2024/real/dec_01.txt";
    let content = fs::read_to_string(path).expect("Something went wrong reading the file");

    dec_01(content.lines());
}

fn dec_01(lines: Lines) {
    let mut lefts = Vec::new();
    let mut rights = Vec::new();

    for line in lines {
        let mut split = line.split_whitespace();
        if let (Some(left), Some(right), None) = (split.next(), split.next(), split.next()) {
            let left_num: u32 = left.parse().expect("Failed to parse left number");
            let right_num: u32 = right.parse().expect("Failed to parse right number");
            lefts.push(left_num);
            rights.push(right_num);
        }
    }

    lefts.sort();
    rights.sort();

    let pairs = lefts.into_iter().zip(rights);

    let result_1: u32 = pairs.map(|pair| pair.0.abs_diff(pair.1)).sum();
    println!("{result_1}")
}
