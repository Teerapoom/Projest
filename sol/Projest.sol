// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

contract ProductInfo {
    enum ProductType { Half, Full }
    enum SourceType { TypeA, TypeB }

    struct UserInfo {
        uint256 userId;
        string name;
        string userAddress;
        ProductType productType;
        uint256 quantity;
        SourceType sourceType;
    }

    mapping(uint256 => UserInfo) private userInfoMapping;
    uint256[] private userIds;
    uint256 private userCounter = 0;

    function storeUserInfo(
        string memory _name,
        string memory _userAddress,
        ProductType _productType,
        uint256 _quantity,
        SourceType _sourceType
    ) public returns (uint256) {
        uint256 newUserId = ++userCounter;
        UserInfo storage user = userInfoMapping[newUserId];
        user.userId = newUserId;
        user.name = _name;
        user.userAddress = _userAddress;
        user.productType = _productType;
        user.quantity = _quantity;
        user.sourceType = _sourceType;
        
        userIds.push(newUserId);

        return newUserId;
    }

    function getUserInfo(uint256 _userId)
        public
        view
        returns (
            uint256,
            string memory,
            string memory,
            ProductType,
            uint256,
            SourceType
        )
    {
        UserInfo storage user = userInfoMapping[_userId];
        return (
            user.userId,
            user.name,
            user.userAddress,
            user.productType,
            user.quantity,
            user.sourceType
        );
    }

    function getAllUsers() public view returns (UserInfo[] memory) {
        UserInfo[] memory users = new UserInfo[](userIds.length);

        for (uint256 i = 0; i < userIds.length; i++) {
            users[i] = userInfoMapping[userIds[i]];
        }

        return users;
    }
}