<?php
//configure/database.php
define('DB_HOST', 'localhost');
define('DB_USER', 'your_username');
define('DB_PASS', 'your_password');
define('DB_NAME', 'COBRAS_FC');

//database connection class
class Database {
    private $conn;

    public function connect(){
        $this->conn = null;
        try{
            $this->conn = new PDO(
                "mysql:host=".DB_HOST .";dbname=".DB_NAME,
                DB_USER,
                DB_PASS
            );
            $this->conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        }catch(PDOException $e){
            echo "Connection Error: " . $e->getMessage();
        }
        return $this->conn;
    }
}
//models/Team.php
class Team{
    private $conn;
    private $table = 'players';

    public function __construct($db){
        $this->conn = $db;
    }

    //Get all players
    public function getPlayers(){
        $query = "SELECT * FROM". $this->table;
        $stmt = $this->conn->prepare($query);
        $stmt->execute();

        return $stmt;
    }
    //Add new player
    public function addPlayer($name, $position, $number, $bio){
        $query = "INSERT INTO ".$this->table." 
        (name,position, number, bio)
        VALUES(:name, :position, :number, :bio)";
$stmt = $this->conn->prepare($query);

//clean data
$name = htmlspecialchars(strip_tags($name));
$position = htmlspecialchars(strip_tags($position));
$number = htmlspecialchars(strip_tags($number));
$bio = htmlspecialchars(strip_tags($bio));

//Bind data
    $stmt->bindParam(':name', $name);
    $stmt->bindParam(':position', $position);
    $stmt->bindParam(':number', $number);
    $stmt->bindParam(':bio', $bio);
    if($stmt->execute()){
        return true;
    }
    return false;
    }
}

//models/News.php
class News{
    private $conn;
    private $table ='news';

    public function__construct($db){
        $this->conn =$db;
    }

    //Get all news articles
    public function getNews(){
        $query ="SELECT * FROM". $this->table." ORDER BY created_at DESC";
        $stmt = $this->conn->prepare($query);
        $stmt = $stmt->execute();

        return $stmt;
    }
//Add news article
    public function addNews($title, $content, $author){
        $query = "INSERT INTO" . $this->table."
        (title, content, author, created_at)
        VALUES(:title, :content, :author, :NOW())";
    }
}