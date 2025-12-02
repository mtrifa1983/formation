/**
 * Calculates the sum of all elements in an array
 * @param {number[]} nums - Array of numbers to sum
 * @returns {number} The sum of all elements
 */
function sumList(nums) {
    return nums.reduce((sum, num) => sum + num, 0);
}

/**
 * Alternative implementation using a for loop
 * This version doesn't use the built-in reduce() function
 * @param {number[]} nums - Array of numbers to sum
 * @returns {number} The sum of all elements
 */
function sumListLoop(nums) {
    // Initialize a variable to store the sum, starting at 0
    let sum = 0;
    
    // Loop through each element in the nums array
    for (let num of nums) {
        // Add the current element to the sum
        // sum = sum + num is equivalent to sum += num
        sum += num;
    }
    
    // Return the final sum value
    return sum;
}

/**
 * Loop through a list and display the square of each element
 * @param {number[]} nums - Array of numbers
 */
function displaySquares(nums) {
    // Loop through each element in the array
    for (let num of nums) {
        // Calculate the square of the current number (num * num)
        let square = num * num;
        // Display the number and its square
        console.log(`${num}² = ${square}`);
    }
}

/**
 * Alternative using map() to create an array of squares
 * @param {number[]} nums - Array of numbers
 * @returns {number[]} Array of squared values
 */
function getSquares(nums) {
    // Use map() to transform each element by multiplying it by itself
    return nums.map(num => num * num);
}

// Test cases
console.log("Testing sumList function:");
console.log("sumList([1, 2, 3, 4, 5]) =", sumList([1, 2, 3, 4, 5]));          // Output: 15
console.log("sumList([10, 20, 30]) =", sumList([10, 20, 30]));                // Output: 60
console.log("sumList([-1, -2, -3]) =", sumList([-1, -2, -3]));                // Output: -6
console.log("sumList([]) =", sumList([]));                                    // Output: 0
console.log("sumList([0]) =", sumList([0]));                                  // Output: 0

console.log("\nTesting sumListLoop function:");
console.log("sumListLoop([1, 2, 3, 4, 5]) =", sumListLoop([1, 2, 3, 4, 5]));  // Output: 15
console.log("sumListLoop([100, 200]) =", sumListLoop([100, 200]));            // Output: 300

console.log("\n--- Testing displaySquares function ---");
console.log("Squares of [1, 2, 3, 4, 5]:");
displaySquares([1, 2, 3, 4, 5]);

console.log("\n--- Testing getSquares function ---");
console.log("getSquares([1, 2, 3, 4, 5]) =", getSquares([1, 2, 3, 4, 5]));    // Output: [1, 4, 9, 16, 25]
console.log("getSquares([10, 20]) =", getSquares([10, 20]));                  // Output: [100, 400]

// Export functions for use as a module
module.exports = { sumList, sumListLoop };

