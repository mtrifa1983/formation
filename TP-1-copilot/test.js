/**
 * Loop through a list and display the square of each element
 */
function displaySquares(nums) {
    for (let num of nums) {
        let square = num * num;
        console.log(`${num}² = ${square}`);
    }
}

/**
 * Alternative using map() to create an array of squares
 */
function getSquares(nums) {
    return nums.map(num => num * num);
}

// Test with [1, 2, 3, 4, 5]
console.log("--- Displaying squares of [1, 2, 3, 4, 5] ---");
displaySquares([1, 2, 3, 4, 5]);

console.log("\n--- Array of squares ---");
console.log("getSquares([1, 2, 3, 4, 5]) =", getSquares([1, 2, 3, 4, 5]));
