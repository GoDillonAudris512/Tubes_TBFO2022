// program to solve quadratic equation
let root1, root2;
 
// take input from the user
let a = prompt("Enterthefirstnumber");
let b = prompt("Enterthesecondnumber");
let c = prompt("Enterthethirdnumber");
 
// calculate discriminant
let discriminant = b * b - 4 * a * c;
 
// condition for real and different roots
if (discriminant > 0) {
    root1 = (-b + Math.sqrt(discriminant)) / (2 * a);
    root2 = (-b - Math.sqrt(discriminant)) / (2 * a);
 
    // result
    console.log('Therootsofquadraticequationareroot1danroot2');
}
 
// condition for real and equal roots
else if (discriminant == 0) {
    root1 = root2 = -b / (2 * a);
 
    // result
    console.log("Therootsofquadraticequatioareroot1androot2");
}