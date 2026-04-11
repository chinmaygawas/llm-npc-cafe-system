using Unity.Cinemachine;
using UnityEngine;
using TMPro;
using System.Collections;

public class MapTransition : MonoBehaviour
{
    [SerializeField] PolygonCollider2D mapBoundary;
    CinemachineConfiner2D confiner;
    [SerializeField] Direction direction;
    [SerializeField] float additivePos = 2f;
    [SerializeField] Transform teleportTargetPosition;
    [SerializeField] GameObject notificationCanvas;
    [SerializeField] TMP_Text notificationText;
    public GameObject dialogueCanvas;

    enum Direction { Up, Down, Left, Right, Teleport }

    private void Awake()
    {
        confiner = FindAnyObjectByType<CinemachineConfiner2D>();
    }

    private void OnTriggerEnter2D(Collider2D collision)
    {
        if (!collision.gameObject.CompareTag("Player"))
            return;

        // ?? BANNED BLOCK
        if (GameState.cafeBanned)
        {
            dialogueCanvas.SetActive(false);

            Debug.Log("Cafe banned = " + GameState.cafeBanned);

            StartCoroutine(ShowNotification("You are banned from this cafe."));

            // push the player slightly away from the entrance
            collision.transform.position += Vector3.down * 0.5f;


            return;
        }

        // normal transition
        confiner.BoundingShape2D = mapBoundary;
        UpdatePlayerPosition(collision.gameObject);
    }

    private void UpdatePlayerPosition(GameObject player)
    {
        if (direction == Direction.Teleport)
        {
            player.transform.position = teleportTargetPosition.position;
            return;
        }

        Vector3 newPos = player.transform.position;

        switch (direction)
        {
            case Direction.Up:
                newPos.y += additivePos;
                break;

            case Direction.Down:
                newPos.y -= additivePos;
                break ;

            case Direction.Left:
                newPos.x += additivePos;
                break;

            case Direction.Right:
                newPos.x -= additivePos;
                break;
        }

        player.transform.position = newPos;
    }

    IEnumerator ShowNotification(string message)
    {
        notificationCanvas.SetActive(true);
        notificationText.text = message;

        yield return new WaitForSeconds(5f);

        notificationCanvas.SetActive(false);
    }
}
