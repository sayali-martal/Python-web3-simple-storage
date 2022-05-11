// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

contract SimpleStorage {
    // Define a variable with type number
    uint256 favNumber;

    // Define Structure
    struct People {
        uint256 favNumber;
        string name;
    }

    // Define dynamic array
    People[] public people;

    // Define mapping
    mapping(string => uint256) public nameToFavNumber;

    // Function to store number
    function store(uint256 _favNumber) public {
        favNumber = _favNumber;
    }

    // Function to return number
    function retrieve() public view returns(uint256) {
        return favNumber;
    }

    // Add entries to array and mappings
    function addPerson(string memory _name, uint256 _favNumber) public {
        people.push(People(_favNumber, _name));
        nameToFavNumber[_name] = _favNumber;
    }
}
