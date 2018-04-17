db.createUser(
{
    user: "hospital",
    pwd: "hospital",
    roles: [
      { role: "readWrite", db: "hospital" }
    ]
})
